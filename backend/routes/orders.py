"""
Orders and checkout routes.
APIs:
- POST /api/orders
- GET  /api/orders/<user_id>
- GET  /api/orders/<user_id>/<order_id>
"""

import uuid
from datetime import datetime, timezone
from flask import Blueprint, request
from database import (
    get_orders_collection,
    get_carts_collection,
    get_products_collection
)
from utils.helpers import (
    success_response,
    error_response,
    serialize_doc,
    serialize_docs,
    is_valid_object_id,
    to_object_id
)

orders_bp = Blueprint("orders", __name__)

ALLOWED_STATUSES = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]


def _find_product(product_id):
    """Finds product by ObjectId or product_id string."""
    products_coll = get_products_collection()
    query = {}
    if is_valid_object_id(product_id):
        query = {"$or": [{"_id": to_object_id(product_id)}, {"product_id": str(product_id)}]}
    else:
        query = {"product_id": str(product_id)}
    return products_coll.find_one(query)


@orders_bp.route("/api/orders", methods=["POST"])
def create_order():
    """
    Places an order for a user.
    Order can be placed from user's current cart, or by specifying items directly.

    Expects JSON body:
    {
        "user_id": "...",
        "shipping_address": {
            "full_name": "Jane Doe",
            "street": "123 Campus Way",
            "city": "University City",
            "state": "State",
            "postal_code": "12345",
            "phone": "555-123-4567"
        },
        "payment_method": "Cash on Delivery",  # Demo checkout
        "items": [...]  # Optional, falls back to user's saved cart
    }

    CRITICAL RULES:
    1. Product prices are ALWAYS taken from MongoDB, NEVER trusted from the frontend.
    2. Product stock is validated before creating the order.
    3. Product stock is decremented in MongoDB upon order placement.
    4. The user's cart is cleared after the order is saved.
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    user_id = str(data.get("user_id", "")).strip()
    shipping_address = data.get("shipping_address")
    payment_method = data.get("payment_method", "Cash on Delivery (Demo Checkout)")

    if not user_id:
        return error_response("user_id is required to place an order", 400)

    if not shipping_address:
        return error_response("shipping_address is required to place an order", 400)

    # If shipping_address is string or dict, validate non-empty
    if isinstance(shipping_address, dict):
        if not any(str(v).strip() for v in shipping_address.values()):
            return error_response("shipping_address cannot be empty", 400)
    elif isinstance(shipping_address, str):
        if not shipping_address.strip():
            return error_response("shipping_address cannot be empty", 400)
    else:
        return error_response("Invalid shipping_address format", 400)

    # Retrieve items: either explicitly supplied or from user's cart
    request_items = data.get("items")
    carts_coll = get_carts_collection()
    user_cart = carts_coll.find_one({"user_id": user_id})

    items_to_order = []
    if request_items and isinstance(request_items, list) and len(request_items) > 0:
        items_to_order = request_items
    elif user_cart and len(user_cart.get("items", [])) > 0:
        items_to_order = user_cart.get("items", [])
    else:
        return error_response("Cannot place order: Cart is empty and no items were provided.", 400)

    # Fetch current product details from MongoDB and validate stock
    products_coll = get_products_collection()
    validated_items = []
    total_amount = 0.0

    for item in items_to_order:
        product_id = item.get("product_id") or item.get("_id")
        try:
            quantity = int(item.get("quantity", 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            continue

        product = _find_product(product_id)
        if not product:
            return error_response(f"Product with ID '{product_id}' was not found in the catalog.", 404)

        current_stock = int(product.get("stock", 0))
        product_name = product.get("name", "Product")

        # Validate stock
        if current_stock < quantity:
            return error_response(
                message=f"Insufficient stock for '{product_name}'. Requested: {quantity}, Available: {current_stock}.",
                status_code=400
            )

        # Always use actual price from MongoDB!
        db_price = float(product.get("price", 0.0))
        item_subtotal = round(db_price * quantity, 2)
        total_amount += item_subtotal

        validated_items.append({
            "product_id": str(product.get("_id")),
            "name": product_name,
            "category": product.get("category", "General"),
            "price": db_price,
            "quantity": quantity,
            "subtotal": item_subtotal,
            "image_url": product.get("image_url", "")
        })

    if not validated_items:
        return error_response("No valid items to order", 400)

    total_amount = round(total_amount, 2)

    # Generate a unique human-friendly order ID
    order_timestamp = datetime.now(timezone.utc)
    order_id = f"ORD-{order_timestamp.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    order_doc = {
        "order_id": order_id,
        "user_id": user_id,
        "items": validated_items,
        "total_amount": total_amount,
        "order_date": order_timestamp,
        "status": "Pending",  # Initial status
        "shipping_address": shipping_address,
        "payment_method": payment_method,
        "created_at": order_timestamp
    }

    orders_coll = get_orders_collection()
    orders_coll.insert_one(order_doc)

    # Deduct stock for each product
    for v_item in validated_items:
        p_id = v_item["product_id"]
        p_query = {}
        if is_valid_object_id(p_id):
            p_query = {"$or": [{"_id": to_object_id(p_id)}, {"product_id": p_id}]}
        else:
            p_query = {"product_id": p_id}

        products_coll.update_one(
            p_query,
            {"$inc": {"stock": -v_item["quantity"]}}
        )

    # Clear user's cart in database
    carts_coll.update_one(
        {"user_id": user_id},
        {"$set": {
            "items": [],
            "total_price": 0.0,
            "total_items": 0,
            "updated_at": order_timestamp
        }},
        upsert=True
    )

    serialized_order = serialize_doc(order_doc)
    return success_response(
        message="Order placed successfully! Your cart has been cleared.",
        data=serialized_order,
        status_code=201
    )


@orders_bp.route("/api/orders/<user_id>", methods=["GET"])
def get_user_orders(user_id):
    """
    Returns order history for a specific user, sorted from newest to oldest.
    """
    if not user_id:
        return error_response("User ID is required", 400)

    orders_coll = get_orders_collection()
    cursor = orders_coll.find({"user_id": str(user_id)}).sort("created_at", -1)

    orders = list(cursor)
    serialized = serialize_docs(orders)

    return success_response(
        message=f"Found {len(serialized)} orders for user",
        data={
            "user_id": str(user_id),
            "orders": serialized,
            "total": len(serialized)
        },
        status_code=200
    )


@orders_bp.route("/api/orders/<user_id>/<order_id>", methods=["GET"])
def get_order_details(user_id, order_id):
    """
    Returns details of a specific order belonging to a user.
    """
    if not user_id or not order_id:
        return error_response("Both user_id and order_id are required", 400)

    orders_coll = get_orders_collection()

    query = {
        "user_id": str(user_id),
        "$or": [
            {"order_id": str(order_id)},
            {"_id": to_object_id(order_id) if is_valid_object_id(order_id) else str(order_id)}
        ]
    }

    order = orders_coll.find_one(query)
    if not order:
        return error_response(f"Order '{order_id}' was not found for this user", 404)

    serialized = serialize_doc(order)
    return success_response(
        message="Order details retrieved successfully",
        data=serialized,
        status_code=200
    )
