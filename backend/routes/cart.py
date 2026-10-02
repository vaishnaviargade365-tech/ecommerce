"""
Shopping cart routes.
APIs:
- GET    /api/cart/<user_id>
- POST   /api/cart
- PUT    /api/cart/<user_id>/<product_id>
- DELETE /api/cart/<user_id>/<product_id>
- DELETE /api/cart/<user_id> (clear full cart)
"""

from datetime import datetime, timezone
from flask import Blueprint, request
from database import get_carts_collection, get_products_collection
from utils.helpers import (
    success_response,
    error_response,
    serialize_doc,
    is_valid_object_id,
    to_object_id
)

cart_bp = Blueprint("cart", __name__)


def _find_product(product_id):
    """Helper to find product by ObjectId or product_id string."""
    products_coll = get_products_collection()
    query = {}
    if is_valid_object_id(product_id):
        query = {"$or": [{"_id": to_object_id(product_id)}, {"product_id": str(product_id)}]}
    else:
        query = {"product_id": str(product_id)}
    return products_coll.find_one(query)


def _recalculate_cart(items):
    """
    Recalculates subtotals and total price based on item prices and quantities.
    Returns (updated_items, total_price, total_items).
    """
    total_price = 0.0
    total_items = 0
    updated_items = []

    for item in items:
        qty = int(item.get("quantity", 1))
        price = float(item.get("price", 0.0))
        subtotal = round(price * qty, 2)
        total_price += subtotal
        total_items += qty

        updated_items.append({
            "product_id": str(item.get("product_id")),
            "name": item.get("name", "Product"),
            "price": price,
            "quantity": qty,
            "subtotal": subtotal,
            "image_url": item.get("image_url", ""),
            "stock": int(item.get("stock", 0))
        })

    return updated_items, round(total_price, 2), total_items


@cart_bp.route("/api/cart/<user_id>", methods=["GET"])
def get_cart(user_id):
    """
    Returns the user's shopping cart.
    Recalculates totals and checks current product prices and stocks from database.
    """
    if not user_id:
        return error_response("User ID is required", 400)

    carts_coll = get_carts_collection()
    cart = carts_coll.find_one({"user_id": str(user_id)})

    if not cart:
        # Return empty cart structure
        return success_response(
            message="Cart is empty",
            data={
                "user_id": str(user_id),
                "items": [],
                "total_price": 0.0,
                "total_items": 0
            },
            status_code=200
        )

    # Refresh current product prices & stocks from DB
    items = cart.get("items", [])
    refreshed_items = []
    for item in items:
        prod = _find_product(item.get("product_id"))
        if prod:
            item["price"] = float(prod.get("price", item.get("price", 0.0)))
            item["name"] = prod.get("name", item.get("name"))
            item["image_url"] = prod.get("image_url", item.get("image_url"))
            item["stock"] = int(prod.get("stock", 0))
            refreshed_items.append(item)

    updated_items, total_price, total_items = _recalculate_cart(refreshed_items)

    # Update cart in database
    carts_coll.update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items,
            "updated_at": datetime.now(timezone.utc)
        }}
    )

    return success_response(
        message="Cart retrieved successfully",
        data={
            "user_id": str(user_id),
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items
        },
        status_code=200
    )


@cart_bp.route("/api/cart", methods=["POST"])
def add_to_cart():
    """
    Adds a product to the user's cart.
    Expects JSON body:
    {
        "user_id": "...",
        "product_id": "...",
        "quantity": 1
    }
    Validates stock availability before adding.
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    user_id = str(data.get("user_id", "")).strip()
    product_id = str(data.get("product_id", "")).strip()

    try:
        quantity = int(data.get("quantity", 1))
    except (ValueError, TypeError):
        return error_response("Quantity must be a positive integer", 400)

    if not user_id:
        return error_response("user_id is required", 400)
    if not product_id:
        return error_response("product_id is required", 400)
    if quantity <= 0:
        return error_response("Quantity must be at least 1", 400)

    # Fetch product from database
    product = _find_product(product_id)
    if not product:
        return error_response("Product not found", 404)

    available_stock = int(product.get("stock", 0))
    if available_stock <= 0:
        return error_response(f"Product '{product.get('name')}' is currently out of stock.", 400)

    carts_coll = get_carts_collection()
    cart = carts_coll.find_one({"user_id": user_id})

    items = cart.get("items", []) if cart else []

    # Check if item is already in cart
    existing_item = None
    for item in items:
        if str(item.get("product_id")) == str(product_id) or str(item.get("product_id")) == str(product.get("_id")):
            existing_item = item
            break

    if existing_item:
        new_quantity = existing_item.get("quantity", 0) + quantity
        if new_quantity > available_stock:
            return error_response(
                message=f"Cannot add {quantity} more. Only {available_stock} items available in stock (you already have {existing_item.get('quantity', 0)} in your cart).",
                status_code=400
            )
        existing_item["quantity"] = new_quantity
        existing_item["price"] = float(product.get("price", 0.0))
        existing_item["stock"] = available_stock
    else:
        if quantity > available_stock:
            return error_response(
                message=f"Requested quantity ({quantity}) exceeds available stock ({available_stock}).",
                status_code=400
            )
        items.append({
            "product_id": str(product.get("_id")),
            "name": product.get("name", ""),
            "price": float(product.get("price", 0.0)),
            "quantity": quantity,
            "image_url": product.get("image_url", ""),
            "stock": available_stock
        })

    updated_items, total_price, total_items = _recalculate_cart(items)

    cart_doc = {
        "user_id": user_id,
        "items": updated_items,
        "total_price": total_price,
        "total_items": total_items,
        "updated_at": datetime.now(timezone.utc)
    }

    carts_coll.update_one(
        {"user_id": user_id},
        {"$set": cart_doc},
        upsert=True
    )

    return success_response(
        message="Product added to cart successfully",
        data={
            "user_id": user_id,
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items
        },
        status_code=200
    )


@cart_bp.route("/api/cart/<user_id>/<product_id>", methods=["PUT"])
def update_cart_quantity(user_id, product_id):
    """
    Updates the quantity of a specific product in the cart.
    Expects JSON body:
    {
        "quantity": 2
    }
    If quantity is 0 or negative, the product is removed from the cart.
    """
    if not user_id or not product_id:
        return error_response("Both user_id and product_id are required in the URL", 400)

    data = request.get_json(silent=True)
    if not data or "quantity" not in data:
        return error_response("Request body must contain 'quantity'", 400)

    try:
        new_quantity = int(data.get("quantity"))
    except (ValueError, TypeError):
        return error_response("Quantity must be an integer", 400)

    carts_coll = get_carts_collection()
    cart = carts_coll.find_one({"user_id": str(user_id)})
    if not cart:
        return error_response("Cart not found for this user", 404)

    items = cart.get("items", [])

    # If new_quantity <= 0, remove the item
    if new_quantity <= 0:
        items = [item for item in items if str(item.get("product_id")) != str(product_id)]
    else:
        product = _find_product(product_id)
        if not product:
            return error_response("Product not found", 404)

        available_stock = int(product.get("stock", 0))
        if new_quantity > available_stock:
            return error_response(
                message=f"Requested quantity ({new_quantity}) exceeds available stock ({available_stock}).",
                status_code=400
            )

        found = False
        for item in items:
            if str(item.get("product_id")) == str(product_id):
                item["quantity"] = new_quantity
                item["price"] = float(product.get("price", item.get("price", 0.0)))
                item["stock"] = available_stock
                found = True
                break

        if not found:
            return error_response("Product is not currently in the cart", 404)

    updated_items, total_price, total_items = _recalculate_cart(items)

    carts_coll.update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items,
            "updated_at": datetime.now(timezone.utc)
        }}
    )

    return success_response(
        message="Cart updated successfully",
        data={
            "user_id": str(user_id),
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items
        },
        status_code=200
    )


@cart_bp.route("/api/cart/<user_id>/<product_id>", methods=["DELETE"])
def remove_from_cart(user_id, product_id):
    """
    Removes a single product from the user's cart.
    """
    if not user_id or not product_id:
        return error_response("Both user_id and product_id are required in the URL", 400)

    carts_coll = get_carts_collection()
    cart = carts_coll.find_one({"user_id": str(user_id)})
    if not cart:
        return error_response("Cart not found for this user", 404)

    items = cart.get("items", [])
    original_count = len(items)
    items = [item for item in items if str(item.get("product_id")) != str(product_id)]

    if len(items) == original_count:
        return error_response("Product was not found in the cart", 404)

    updated_items, total_price, total_items = _recalculate_cart(items)

    carts_coll.update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items,
            "updated_at": datetime.now(timezone.utc)
        }}
    )

    return success_response(
        message="Product removed from cart successfully",
        data={
            "user_id": str(user_id),
            "items": updated_items,
            "total_price": total_price,
            "total_items": total_items
        },
        status_code=200
    )


@cart_bp.route("/api/cart/<user_id>", methods=["DELETE"])
def clear_cart(user_id):
    """
    Clears all items from the user's cart.
    """
    if not user_id:
        return error_response("User ID is required", 400)

    carts_coll = get_carts_collection()
    carts_coll.update_one(
        {"user_id": str(user_id)},
        {"$set": {
            "items": [],
            "total_price": 0.0,
            "total_items": 0,
            "updated_at": datetime.now(timezone.utc)
        }},
        upsert=True
    )

    return success_response(
        message="Cart cleared successfully",
        data={
            "user_id": str(user_id),
            "items": [],
            "total_price": 0.0,
            "total_items": 0
        },
        status_code=200
    )
