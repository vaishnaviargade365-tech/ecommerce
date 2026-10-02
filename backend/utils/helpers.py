"""
Utility helpers for the Flask e-commerce backend:
- Standardized JSON responses
- MongoDB document serialization (ObjectId & datetime handling)
- Input validations (email, required fields)
- Beginner-friendly admin authorization check
"""

import re
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from bson import ObjectId
from bson.errors import InvalidId


def success_response(message="Success", data=None, status_code=200):
    """
    Standardized success JSON response.
    Format:
    {
        "success": True,
        "message": "...",
        "data": ...
    }
    """
    body = {
        "success": True,
        "message": message
    }
    if data is not None:
        body["data"] = data
    return jsonify(body), status_code


def error_response(message="An error occurred", status_code=400, errors=None):
    """
    Standardized error JSON response.
    Format:
    {
        "success": False,
        "message": "...",
        "errors": ... (optional)
    }
    """
    body = {
        "success": False,
        "message": message
    }
    if errors is not None:
        body["errors"] = errors
    return jsonify(body), status_code


def serialize_doc(doc):
    """
    Recursively converts MongoDB BSON types (ObjectId, datetime) into JSON-serializable types.
    Ensures that '_id' is converted to a string and also creates a friendly 'id' or 'product_id'.
    """
    if doc is None:
        return None

    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]

    if not isinstance(doc, dict):
        if isinstance(doc, ObjectId):
            return str(doc)
        if isinstance(doc, datetime):
            return doc.isoformat()
        return doc

    serialized = {}
    for key, val in doc.items():
        if isinstance(val, ObjectId):
            serialized[key] = str(val)
        elif isinstance(val, datetime):
            serialized[key] = val.isoformat()
        elif isinstance(val, dict):
            serialized[key] = serialize_doc(val)
        elif isinstance(val, list):
            serialized[key] = [serialize_doc(item) for item in val]
        else:
            serialized[key] = val

    # For convenience, expose string id alongside _id
    if "_id" in serialized:
        serialized["_id"] = str(serialized["_id"])
        # If product without product_id, ensure product_id exists
        if "product_id" not in serialized:
            serialized["product_id"] = serialized["_id"]

    return serialized


def serialize_docs(docs):
    """Serializes a list or cursor of MongoDB documents."""
    return [serialize_doc(doc) for doc in docs]


def validate_email(email):
    """Validates email format using regex."""
    if not email or not isinstance(email, str):
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_regex, email.strip()) is not None


def is_valid_object_id(id_str):
    """Checks whether a string is a valid 24-character hexadecimal ObjectId."""
    try:
        ObjectId(str(id_str))
        return True
    except (InvalidId, TypeError):
        return False


def to_object_id(id_str):
    """Safely converts string to ObjectId, returning None if invalid."""
    try:
        return ObjectId(str(id_str))
    except (InvalidId, TypeError):
        return None


def admin_required(f):
    """
    Beginner-friendly admin verification decorator.
    Inspects:
    1. Header 'X-User-Role: admin'
    2. Header 'X-User-Id: <user_id>' (checks user in database for role=='admin')
    3. Query param '?role=admin' or '?admin_id=<user_id>'
    4. Request JSON body { "admin_id": "..." } or { "user_id": "...", "role": "admin" }

    This keeps the API simple and testable with Postman/cURL/frontend
    without needing heavy JWT setup for a college project.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Import lazily to avoid circular dependency
        from database import get_users_collection

        # 1. Direct role check in header
        role_header = request.headers.get("X-User-Role", "").strip().lower()
        if role_header == "admin":
            return f(*args, **kwargs)

        # 2. Query param role
        role_param = request.args.get("role", "").strip().lower()
        if role_param == "admin":
            return f(*args, **kwargs)

        # 3. User ID lookup in header, query, or body
        user_id = (
            request.headers.get("X-User-Id")
            or request.headers.get("X-Admin-Id")
            or request.args.get("admin_id")
            or request.args.get("user_id")
        )

        # Check body if JSON
        if not user_id and request.is_json:
            data = request.get_json(silent=True) or {}
            user_id = data.get("admin_id") or data.get("user_id")
            if data.get("role") == "admin":
                return f(*args, **kwargs)

        if user_id:
            users_coll = get_users_collection()
            query = {}
            if is_valid_object_id(user_id):
                query = {"_id": to_object_id(user_id)}
            else:
                query = {"_id": user_id}

            user = users_coll.find_one(query)
            if user and user.get("role") == "admin":
                return f(*args, **kwargs)

        return error_response(
            message="Forbidden: Admin access required. Provide 'X-User-Role: admin' header or valid admin credentials.",
            status_code=403
        )

    return decorated_function
