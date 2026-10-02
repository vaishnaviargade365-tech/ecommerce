"""
Verification script for MongoDB Atlas connection and Flask configuration.
Validates:
1. Loading of .env configuration.
2. Safe PyMongo connection to MongoDB Atlas.
3. Access to 'ecommerce_db' database and collection indexing.
4. Product seeding if database is empty.
5. API endpoint verification (e.g. GET /api/products).
"""

import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from database import test_connection, get_db, init_db, get_products_collection
from seed_data import seed_database
from app import create_app


def run_verification():
    print("=" * 60)
    print("  VERIFYING BACKEND & MONGODB ATLAS CONNECTION")
    print("=" * 60)

    # 1. Verify .env loading
    print("\n[Step 1] Verifying .env configuration...")
    if not Config.MONGO_URI:
        print("ERROR: MONGO_URI is not set in environment.")
        return False

    print(" -> .env loaded successfully.")
    print(f" -> Target Database: {Config.DB_NAME}")
    print(f" -> Port Configured: {Config.PORT}")
    print(f" -> Environment: {Config.FLASK_ENV}")

    # 2. Test MongoDB Atlas Connection
    print("\n[Step 2] Testing MongoDB Atlas connection via PyMongo...")
    connected, message = test_connection()
    if not connected:
        print(f"ERROR: Could not connect to MongoDB Atlas:\n{message}")
        return False

    print(" -> MongoDB Atlas connection verified successfully! (Ping succeeded)")

    # 3. Verify 'ecommerce_db' database & create indexes
    print("\n[Step 3] Verifying 'ecommerce_db' database & initializing indexes...")
    db = get_db()
    print(f" -> Connected to database: '{db.name}'")
    init_db()

    # 4. Check / Seed Products
    print("\n[Step 4] Checking products in database...")
    products_coll = get_products_collection()
    product_count = products_coll.count_documents({})
    if product_count == 0:
        print(" -> Products collection is empty. Seeding initial demo products...")
        seed_database()
        product_count = products_coll.count_documents({})

    print(f" -> Verified 'ecommerce_db.products' collection contains {product_count} products.")

    # 5. Test Flask application and API endpoint (GET /api/products)
    print("\n[Step 5] Testing Flask API endpoint (GET /api/products)...")
    app = create_app()
    with app.test_client() as client:
        # Test Health Check
        health_res = client.get("/api/health")
        assert health_res.status_code == 200, f"Health check returned status {health_res.status_code}"
        print(" -> GET /api/health returned 200 OK (Healthy).")

        # Test Products Endpoint
        prod_res = client.get("/api/products")
        assert prod_res.status_code == 200, f"GET /api/products returned status {prod_res.status_code}"
        prod_json = prod_res.get_json()
        assert prod_json["success"] is True
        total = prod_json["data"]["total"]
        print(f" -> GET /api/products returned 200 OK with {total} products in JSON format.")

    print("\n" + "=" * 60)
    print("  ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_verification()
    if not success:
        sys.exit(1)
