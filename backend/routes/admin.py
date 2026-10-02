"""
Admin management routes.
APIs:
- GET    /api/admin/products               (View all products with inventory status)
- POST   /api/admin/products               (Add new product)
- PUT    /api/admin/products/<product_id>  (Update product details)
- DELETE /api/admin/products/<product_id>  (Delete product)
- PATCH  /api/admin/products/<product_id>/stock (Update product stock)
- GET    /api/admin/orders                 (View all customer orders)
- PATCH  /api/admin/orders/<order_id>/status (Update order status)
- GET    /api/admin/stats                  (Dashboard summary statistics)
"""

from datetime import datetime, timezone
from flask import Blueprint, request
from database import (
    get_products_collection,
    get_orders_collection,
    get_users_collection
)
from utils.helpers import (
    success_response,
    error_response,
    serialize_doc,
    serialize_docs,
    is_valid_object_id,
    to_object_id,
    admin_required
)

admin_bp = Blueprint("admin", __name__)

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


@admin_bp.route("/api/admin/products", methods=["GET"])
@admin_required
def admin_get_all_products():
    """
    Returns all products in the database including inventory details.
    """
    products_coll = get_products_collection()
    products = list(products_coll.find().sort("_id", -1))
    serialized = serialize_docs(products)

    return success_response(
        message=f"Retrieved {len(serialized)} products for admin",
        data={
            "products": serialized,
            "total": len(serialized)
        },
        status_code=200
    )


@admin_bp.route("/api/admin/products", methods=["POST"])
@admin_required
def admin_add_product():
    """
    Adds a new product to the catalog.
    Expects JSON body:
    {
        "name": "Wireless Headphones",
        "description": "Premium noise cancelling headphones",
        "category": "Electronics",
        "price": 149.99,
        "image_url": "https://example.com/headphones.jpg",
        "stock": 25,
        "rating": 4.8
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    name = str(data.get("name", "")).strip()
    description = str(data.get("description", "")).strip()
    category = str(data.get("category", "")).strip()
    image_url = str(data.get("image_url", "")).strip()

    # Numeric validations
    try:
        price = float(data.get("price", 0))
    except (ValueError, TypeError):
        return error_response("Price must be a valid number", 400)

    try:
        stock = int(data.get("stock", 0))
    except (ValueError, TypeError):
        return error_response("Stock must be an integer", 400)

    try:
        rating = float(data.get("rating", 4.5))
    except (ValueError, TypeError):
        rating = 4.5

    errors = []
    if not name:
        errors.append("Product name is required.")
    if not description:
        errors.append("Product description is required.")
    if not category:
        errors.append("Product category is required.")
    if price <= 0:
        errors.append("Price must be greater than 0.")
    if stock < 0:
        errors.append("Stock cannot be negative.")

    if errors:
        return error_response(
            message="Product validation failed",
            status_code=400,
            errors=errors
        )

    products_coll = get_products_collection()

    product_doc = {
        "name": name,
        "description": description,
        "category": category,
        "price": round(price, 2),
        "image_url": image_url or "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "stock": stock,
        "rating": round(min(max(rating, 0.0), 5.0), 1),
        "created_at": datetime.now(timezone.utc)
    }

    result = products_coll.insert_one(product_doc)
    product_id = str(result.inserted_id)

    # Store string product_id as well for convenience
    products_coll.update_one({"_id": result.inserted_id}, {"$set": {"product_id": product_id}})
    product_doc["product_id"] = product_id

    return success_response(
        message="Product added successfully",
        data=serialize_doc(product_doc),
        status_code=201
    )


@admin_bp.route("/api/admin/products/<product_id>", methods=["PUT"])
@admin_required
def admin_update_product(product_id):
    """
    Updates an existing product.
    Accepts partial or full update fields:
    name, description, category, price, image_url, stock, rating
    """
    if not product_id:
        return error_response("Product ID is required in URL", 400)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    existing = _find_product(product_id)
    if not existing:
        return error_response(f"Product '{product_id}' not found", 404)

    update_fields = {}

    if "name" in data and str(data["name"]).strip():
        update_fields["name"] = str(data["name"]).strip()

    if "description" in data and str(data["description"]).strip():
        update_fields["description"] = str(data["description"]).strip()

    if "category" in data and str(data["category"]).strip():
        update_fields["category"] = str(data["category"]).strip()

    if "image_url" in data:
        update_fields["image_url"] = str(data["image_url"]).strip()

    if "price" in data:
        try:
            price = float(data["price"])
            if price <= 0:
                return error_response("Price must be greater than 0", 400)
            update_fields["price"] = round(price, 2)
        except (ValueError, TypeError):
            return error_response("Invalid price value", 400)

    if "stock" in data:
        try:
            stock = int(data["stock"])
            if stock < 0:
                return error_response("Stock cannot be negative", 400)
            update_fields["stock"] = stock
        except (ValueError, TypeError):
            return error_response("Invalid stock value", 400)

    if "rating" in data:
        try:
            rating = float(data["rating"])
            update_fields["rating"] = round(min(max(rating, 0.0), 5.0), 1)
        except (ValueError, TypeError):
            pass

    if not update_fields:
        return error_response("No valid fields provided to update", 400)

    update_fields["updated_at"] = datetime.now(timezone.utc)

    products_coll = get_products_collection()
    query = {"_id": existing["_id"]}

    products_coll.update_one(query, {"$set": update_fields})
    updated_doc = products_coll.find_one(query)

    return success_response(
        message="Product updated successfully",
        data=serialize_doc(updated_doc),
        status_code=200
    )


@admin_bp.route("/api/admin/products/<product_id>", methods=["DELETE"])
@admin_required
def admin_delete_product(product_id):
    """
    Deletes a product from the database catalog.
    """
    if not product_id:
        return error_response("Product ID is required in URL", 400)

    existing = _find_product(product_id)
    if not existing:
        return error_response(f"Product '{product_id}' not found", 404)

    products_coll = get_products_collection()
    products_coll.delete_one({"_id": existing["_id"]})

    return success_response(
        message=f"Product '{existing.get('name')}' deleted successfully",
        data={"deleted_product_id": str(existing["_id"])},
        status_code=200
    )


@admin_bp.route("/api/admin/products/<product_id>/stock", methods=["PATCH", "PUT"])
@admin_required
def admin_update_stock(product_id):
    """
    Updates the inventory stock level of a product.
    Expects JSON body:
    {
        "stock": 40
    }
    """
    if not product_id:
        return error_response("Product ID is required in URL", 400)

    data = request.get_json(silent=True)
    if not data or "stock" not in data:
        return error_response("Request body must contain 'stock'", 400)

    try:
        new_stock = int(data.get("stock"))
        if new_stock < 0:
            return error_response("Stock cannot be negative", 400)
    except (ValueError, TypeError):
        return error_response("Stock must be a non-negative integer", 400)

    existing = _find_product(product_id)
    if not existing:
        return error_response(f"Product '{product_id}' not found", 404)

    products_coll = get_products_collection()
    products_coll.update_one(
        {"_id": existing["_id"]},
        {"$set": {
            "stock": new_stock,
            "updated_at": datetime.now(timezone.utc)
        }}
    )

    updated_doc = products_coll.find_one({"_id": existing["_id"]})

    return success_response(
        message=f"Stock for '{existing.get('name')}' updated to {new_stock}",
        data=serialize_doc(updated_doc),
        status_code=200
    )


@admin_bp.route("/api/admin/orders", methods=["GET"])
@admin_required
def admin_get_all_orders():
    """
    Returns all customer orders across the platform, sorted from newest to oldest.
    """
    orders_coll = get_orders_collection()
    orders = list(orders_coll.find().sort("created_at", -1))
    serialized = serialize_docs(orders)

    return success_response(
        message=f"Retrieved {len(serialized)} customer orders",
        data={
            "orders": serialized,
            "total": len(serialized)
        },
        status_code=200
    )


@admin_bp.route("/api/admin/orders/<order_id>/status", methods=["PATCH", "PUT"])
@admin_required
def admin_update_order_status(order_id):
    """
    Updates the status of a customer order.
    Expects JSON body:
    {
        "status": "Shipped"
    }
    Allowed statuses: Pending, Confirmed, Shipped, Delivered, Cancelled
    """
    if not order_id:
        return error_response("Order ID is required in URL", 400)

    data = request.get_json(silent=True)
    if not data or "status" not in data:
        return error_response("Request body must contain 'status'", 400)

    new_status = str(data.get("status", "")).strip().capitalize()
    if new_status not in ALLOWED_STATUSES:
        return error_response(
            message=f"Invalid status '{new_status}'. Allowed values are: {', '.join(ALLOWED_STATUSES)}",
            status_code=400
        )

    orders_coll = get_orders_collection()

    query = {
        "$or": [
            {"order_id": str(order_id)},
            {"_id": to_object_id(order_id) if is_valid_object_id(order_id) else str(order_id)}
        ]
    }

    order = orders_coll.find_one(query)
    if not order:
        return error_response(f"Order '{order_id}' was not found", 404)

    orders_coll.update_one(
        {"_id": order["_id"]},
        {"$set": {
            "status": new_status,
            "status_updated_at": datetime.now(timezone.utc)
        }}
    )

    updated_order = orders_coll.find_one({"_id": order["_id"]})

    return success_response(
        message=f"Order status updated from '{order.get('status')}' to '{new_status}'",
        data=serialize_doc(updated_order),
        status_code=200
    )


@admin_bp.route("/api/admin/stats", methods=["GET"])
@admin_required
def admin_get_dashboard_stats():
    """
    Returns high-level statistics for the admin dashboard:
    - total products
    - total orders
    - total revenue
    - total users
    - recent orders summary
    """
    products_coll = get_products_collection()
    orders_coll = get_orders_collection()
    users_coll = get_users_collection()

    total_products = products_coll.count_documents({})
    total_orders = orders_coll.count_documents({})
    total_users = users_coll.count_documents({"role": "user"})

    # Calculate total revenue
    pipeline = [
        {"$match": {"status": {"$ne": "Cancelled"}}},
        {"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}
    ]
    revenue_res = list(orders_coll.aggregate(pipeline))
    total_revenue = round(revenue_res[0]["total_revenue"], 2) if revenue_res else 0.0

    # Low stock alert (stock <= 5)
    low_stock_products = list(products_coll.find({"stock": {"$lte": 5}}))

    return success_response(
        message="Dashboard statistics retrieved successfully",
        data={
            "total_products": total_products,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "total_customers": total_users,
            "low_stock_count": len(low_stock_products)
        },
        status_code=200
    )
