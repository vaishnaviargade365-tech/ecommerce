"""
Authentication and User Profile routes.
APIs:
- POST /api/register (and /api/auth/register)
- POST /api/login    (and /api/auth/login)
- GET  /api/profile/<user_id> (and /api/auth/profile/<user_id>)
"""

from datetime import datetime, timezone
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_users_collection
from utils.helpers import (
    success_response,
    error_response,
    serialize_doc,
    validate_email,
    is_valid_object_id,
    to_object_id
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """
    Registers a new user account.
    Expects JSON body:
    {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "secretpassword",
        "role": "user"  # Optional, defaults to "user" ("admin" allowed for setup)
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    name = data.get("name", "").strip() if isinstance(data.get("name"), str) else ""
    email = data.get("email", "").strip().lower() if isinstance(data.get("email"), str) else ""
    password = data.get("password", "")
    role = data.get("role", "user").strip().lower() if isinstance(data.get("role"), str) else "user"

    # Validation
    errors = []
    if not name:
        errors.append("Name is required and cannot be empty.")
    if not email:
        errors.append("Email is required and cannot be empty.")
    elif not validate_email(email):
        errors.append("Please provide a valid email address (e.g. user@example.com).")
    if not password or not isinstance(password, str):
        errors.append("Password is required.")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters long.")

    if role not in ["user", "admin"]:
        role = "user"

    if errors:
        return error_response(
            message="Validation failed",
            status_code=400,
            errors=errors
        )

    users_coll = get_users_collection()

    # Check if email already exists (case-insensitive check)
    existing_user = users_coll.find_one({"email": email})
    if existing_user:
        return error_response(
            message="An account with this email address already exists. Please log in.",
            status_code=400
        )

    # Hash the password securely using Werkzeug (PBKDF2/SHA256)
    hashed_password = generate_password_hash(password, method="scrypt")

    user_doc = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "role": role,
        "created_at": datetime.now(timezone.utc)
    }

    result = users_coll.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Return safe user data (NEVER return password)
    return success_response(
        message="User registered successfully",
        data={
            "user_id": user_id,
            "name": name,
            "email": email,
            "role": role
        },
        status_code=201
    )


@auth_bp.route("/api/login", methods=["POST"])
@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Authenticates a user with email and password.
    Expects JSON body:
    {
        "email": "jane@example.com",
        "password": "secretpassword"
    }
    """
    data = request.get_json(silent=True)
    if not data:
        return error_response("Invalid or missing JSON payload in request body", 400)

    email = data.get("email", "").strip().lower() if isinstance(data.get("email"), str) else ""
    password = data.get("password", "")

    if not email or not password:
        return error_response(
            message="Both email and password are required.",
            status_code=400
        )

    users_coll = get_users_collection()
    user = users_coll.find_one({"email": email})

    # Verify user existence and password hash
    if not user or not check_password_hash(user.get("password", ""), str(password)):
        return error_response(
            message="Invalid email or password",
            status_code=401
        )

    # Return user details excluding the password
    user_id = str(user["_id"])
    return success_response(
        message="Login successful",
        data={
            "user_id": user_id,
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "role": user.get("role", "user")
        },
        status_code=200
    )


@auth_bp.route("/api/profile/<user_id>", methods=["GET"])
@auth_bp.route("/api/auth/profile/<user_id>", methods=["GET"])
def get_profile(user_id):
    """
    Retrieves the basic profile information for a user.
    Never returns password hash.
    """
    if not user_id:
        return error_response("User ID is required", 400)

    users_coll = get_users_collection()

    query = {}
    if is_valid_object_id(user_id):
        query = {"_id": to_object_id(user_id)}
    else:
        query = {"_id": user_id}

    # Project out the password field
    user = users_coll.find_one(query, {"password": 0})
    if not user:
        return error_response("User profile not found", 404)

    serialized = serialize_doc(user)
    serialized["user_id"] = serialized["_id"]

    return success_response(
        message="User profile retrieved successfully",
        data=serialized,
        status_code=200
    )
