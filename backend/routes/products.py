"""
Products and Category routes.
APIs:
- GET /api/products
- GET /api/products/<product_id>
- GET /api/products/search?q=<search>
- GET /api/products/category/<category>
- GET /api/categories
"""

import re
from flask import Blueprint, request
from database import get_products_collection
from utils.helpers import (
    success_response,
    error_response,
    serialize_doc,
    serialize_docs,
    is_valid_object_id,
    to_object_id
)

products_bp = Blueprint("products", __name__)


@products_bp.route("/api/products", methods=["GET"])
def get_products():
    """
    Returns all products.
    Supports optional query parameters:
    - category: filter by category name
    - search or q: search keyword in name or description
    - sort: price_asc, price_desc, rating_desc
    """
    products_coll = get_products_collection()

    category_filter = request.args.get("category", "").strip()
    search_query = (request.args.get("search") or request.args.get("q") or "").strip()
    sort_by = request.args.get("sort", "").strip()

    filter_dict = {}

    if category_filter:
        # Case-insensitive category match
        filter_dict["category"] = {"$regex": f"^{re.escape(category_filter)}$", "$options": "i"}

    if search_query:
        # Match name or description or category
        regex_pattern = {"$regex": re.escape(search_query), "$options": "i"}
        filter_dict["$or"] = [
            {"name": regex_pattern},
            {"description": regex_pattern},
            {"category": regex_pattern}
        ]

    cursor = products_coll.find(filter_dict)

    if sort_by == "price_asc":
        cursor = cursor.sort("price", 1)
    elif sort_by == "price_desc":
        cursor = cursor.sort("price", -1)
    elif sort_by == "rating_desc":
        cursor = cursor.sort("rating", -1)
    else:
        # Default sort by created_at or _id descending
        cursor = cursor.sort("_id", -1)

    products = list(cursor)
    serialized = serialize_docs(products)

    return success_response(
        message=f"Retrieved {len(serialized)} products",
        data={
            "products": serialized,
            "total": len(serialized)
        },
        status_code=200
    )


@products_bp.route("/api/products/search", methods=["GET"])
def search_products():
    """
    Search products by keyword in name, category, or description.
    Example: GET /api/products/search?q=wireless
    """
    query_str = (request.args.get("q") or request.args.get("search") or "").strip()
    if not query_str:
        return error_response("Search query parameter 'q' is required", 400)

    products_coll = get_products_collection()
    regex_pattern = {"$regex": re.escape(query_str), "$options": "i"}

    cursor = products_coll.find({
        "$or": [
            {"name": regex_pattern},
            {"description": regex_pattern},
            {"category": regex_pattern}
        ]
    })

    products = list(cursor)
    serialized = serialize_docs(products)

    return success_response(
        message=f"Found {len(serialized)} products matching '{query_str}'",
        data={
            "products": serialized,
            "total": len(serialized),
            "query": query_str
        },
        status_code=200
    )


@products_bp.route("/api/products/category/<category>", methods=["GET"])
def get_products_by_category(category):
    """
    Filter products by category name (case-insensitive).
    Example: GET /api/products/category/Electronics
    """
    if not category:
        return error_response("Category name is required", 400)

    products_coll = get_products_collection()
    category_regex = {"$regex": f"^{re.escape(category)}$", "$options": "i"}

    cursor = products_coll.find({"category": category_regex})
    products = list(cursor)
    serialized = serialize_docs(products)

    return success_response(
        message=f"Retrieved {len(serialized)} products in category '{category}'",
        data={
            "category": category,
            "products": serialized,
            "total": len(serialized)
        },
        status_code=200
    )


@products_bp.route("/api/products/<product_id>", methods=["GET"])
def get_product_by_id(product_id):
    """
    Returns a single product by its ID.
    Accepts MongoDB ObjectId or custom product_id string.
    """
    if not product_id:
        return error_response("Product ID is required", 400)

    products_coll = get_products_collection()

    query = {}
    if is_valid_object_id(product_id):
        query = {"$or": [{"_id": to_object_id(product_id)}, {"product_id": product_id}]}
    else:
        query = {"product_id": product_id}

    product = products_coll.find_one(query)
    if not product:
        return error_response("Product not found", 404)

    serialized = serialize_doc(product)
    return success_response(
        message="Product details retrieved successfully",
        data=serialized,
        status_code=200
    )


@products_bp.route("/api/categories", methods=["GET"])
def get_categories():
    """
    Returns a distinct list of product categories available in the store with count.
    """
    products_coll = get_products_collection()

    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    try:
        results = list(products_coll.aggregate(pipeline))
        categories = [{"name": r["_id"], "count": r["count"]} for r in results if r["_id"]]
    except Exception:
        # Fallback to distinct if aggregation is not supported by mock
        distinct_cats = products_coll.distinct("category")
        categories = [{"name": cat, "count": products_coll.count_documents({"category": cat})} for cat in distinct_cats if cat]

    return success_response(
        message="Categories retrieved successfully",
        data={"categories": categories},
        status_code=200
    )
