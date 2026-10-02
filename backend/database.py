"""
Database module for the Flask e-commerce backend.
Manages the PyMongo connection to MongoDB Atlas and provides access to collections:
- users
- products
- carts
- orders
"""

import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError, ServerSelectionTimeoutError
from config import Config

# Global database client and db instances
_client = None
_db = None


def get_client():
    """
    Initializes and returns the PyMongo MongoClient singleton.
    Reads MONGO_URI from Config (populated by .env).
    """
    global _client

    if _client is not None:
        return _client

    mongo_uri = Config.MONGO_URI

    # Check if a custom mock client is injected for testing
    if os.getenv("USE_MOCK_DB", "false").lower() == "true":
        try:
            import mongomock
            print("[Database] Using in-memory mongomock database for testing.")
            _client = mongomock.MongoClient()
            return _client
        except ImportError:
            print("[Database] mongomock not installed, proceeding with real PyMongo.")

    try:
        # Create MongoClient with a 5-second server selection timeout for quick feedback
        _client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            retryWrites=True
        )
        return _client
    except (ConfigurationError, Exception) as exc:
        print(f"[Database Error] Could not initialize MongoDB client: {exc}", file=sys.stderr)
        raise


def get_db():
    """
    Returns the database instance for 'ecommerce_db'.
    """
    global _db
    if _db is not None:
        return _db

    client = get_client()
    db_name = Config.DB_NAME
    _db = client[db_name]
    return _db


# Convenience accessors for required collections
def get_users_collection():
    """Returns the 'users' collection."""
    return get_db()["users"]


def get_products_collection():
    """Returns the 'products' collection."""
    return get_db()["products"]


def get_carts_collection():
    """Returns the 'carts' collection."""
    return get_db()["carts"]


def get_orders_collection():
    """Returns the 'orders' collection."""
    return get_db()["orders"]


def test_connection():
    """
    Pings the MongoDB server to verify that the connection works.
    Returns (True, message) if successful, (False, error_message) if it fails.
    """
    try:
        client = get_client()
        # Admin command 'ping' is the standard way to test a MongoDB connection
        client.admin.command("ping")
        return True, "Successfully connected to MongoDB Atlas!"
    except (ServerSelectionTimeoutError, ConnectionFailure) as err:
        return False, (
            f"Could not connect to MongoDB Atlas. Please verify:\n"
            f"1. Your MONGO_URI in .env is correct.\n"
            f"2. Your MongoDB Atlas Network Access allows your IP address (or 0.0.0.0/0).\n"
            f"3. Your database username and password are valid.\n"
            f"Error details: {err}"
        )
    except Exception as err:
        return False, f"Unexpected database error: {err}"


def init_db(app=None):
    """
    Ensures essential indexes exist on collections:
    - users: unique index on 'email'
    - products: index on 'category' and 'name'
    - carts: unique index on 'user_id'
    - orders: index on 'user_id' and 'order_id'
    """
    try:
        users = get_users_collection()
        users.create_index("email", unique=True)

        products = get_products_collection()
        products.create_index("category")
        products.create_index("name")

        carts = get_carts_collection()
        carts.create_index("user_id", unique=True)

        orders = get_orders_collection()
        orders.create_index("user_id")
        orders.create_index("order_id", unique=True)

        print("[Database] Indexes created successfully.")
    except Exception as err:
        print(f"[Database Warning] Could not ensure indexes (continuing): {err}")
