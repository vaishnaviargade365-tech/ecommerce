"""
Live End-to-End API Test Suite for Mini E-Commerce Backend.
Executes real HTTP requests against the running Flask server (http://127.0.0.1:5000)
and verifies that data is actively stored and retrieved from MongoDB Atlas.

Covers all 19 required features:
1.  User registration
2.  User login
3.  Get user profile
4.  Get all products
5.  Get a single product
6.  Search products
7.  Filter products by category
8.  Add product to cart
9.  Update cart quantity
10. Remove product from cart
11. View cart and calculate total
12. Create an order
13. View user order history
14. Admin add product
15. Admin update product
16. Admin delete product
17. Admin update stock
18. Admin view orders
19. Admin update order status
"""

import sys
import os
import time
import uuid
import json
import urllib.request
import urllib.error

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    get_users_collection,
    get_products_collection,
    get_carts_collection,
    get_orders_collection,
    test_connection
)
from utils.helpers import to_object_id

BASE_URL = "http://127.0.0.1:5000"
ADMIN_HEADERS = {
    "Content-Type": "application/json",
    "X-User-Role": "admin"
}
JSON_HEADERS = {
    "Content-Type": "application/json"
}


def http_request(method, endpoint, data=None, headers=None):
    """Utility to make HTTP requests and return (status_code, response_json)."""
    url = f"{BASE_URL}{endpoint}"
    req_headers = dict(headers or JSON_HEADERS)

    req_data = None
    if data is not None:
        req_data = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=req_data, headers=req_headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            return status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8")
        return status, json.loads(body) if body else {}
    except Exception as exc:
        print(f"HTTP request error: {exc}")
        return 0, {"error": str(exc)}


def run_all_tests():
    print("=" * 70)
    print("  EXECUTING LIVE END-TO-END TEST SUITE (19 FEATURES)")
    print(f"  Target Server: {BASE_URL}")
    print("=" * 70)

    # Verify MongoDB Atlas live connection
    conn_ok, conn_msg = test_connection()
    assert conn_ok, f"MongoDB Atlas connection failed: {conn_msg}"
    print("[Atlas] Connected to MongoDB Atlas successfully.")

    users_coll = get_users_collection()
    products_coll = get_products_collection()
    carts_coll = get_carts_collection()
    orders_coll = get_orders_collection()

    results = {}
    test_email = f"test_{int(time.time())}_{uuid.uuid4().hex[:4]}@university.edu"
    test_password = "SecurePassword123!"
    test_name = "Jane Student"
    user_id = None
    test_product_id = None
    second_product_id = None
    created_order_id = None
    admin_prod_id = None

    # -------------------------------------------------------------
    # 1. User registration
    # -------------------------------------------------------------
    print("\n[Feature 1/19] Testing User Registration (POST /api/register)...")
    status, res = http_request("POST", "/api/register", {
        "name": test_name,
        "email": test_email,
        "password": test_password,
        "role": "user"
    })
    assert status == 201, f"Expected 201, got {status}: {res}"
    assert res.get("success") is True
    user_id = res["data"]["user_id"]
    assert "password" not in res["data"]

    # Verify directly in MongoDB Atlas
    db_user = users_coll.find_one({"email": test_email.lower()})
    assert db_user is not None, "User not found in MongoDB Atlas 'users' collection"
    assert db_user["name"] == test_name
    print(f" -> Passed (Status 201). Verified in Atlas collection 'users'.")
    results["1. User registration"] = "Working"

    # -------------------------------------------------------------
    # 2. User login
    # -------------------------------------------------------------
    print("\n[Feature 2/19] Testing User Login (POST /api/login)...")
    status, res = http_request("POST", "/api/login", {
        "email": test_email,
        "password": test_password
    })
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["email"] == test_email.lower()
    assert "password" not in res["data"]
    print(" -> Passed (Status 200). User authenticated successfully.")
    results["2. User login"] = "Working"

    # -------------------------------------------------------------
    # 3. Get user profile
    # -------------------------------------------------------------
    print(f"\n[Feature 3/19] Testing Get User Profile (GET /api/profile/{user_id})...")
    status, res = http_request("GET", f"/api/profile/{user_id}")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["name"] == test_name
    assert "password" not in res["data"]
    print(" -> Passed (Status 200). Profile retrieved without exposing password hash.")
    results["3. Get user profile"] = "Working"

    # -------------------------------------------------------------
    # 4. Get all products
    # -------------------------------------------------------------
    print("\n[Feature 4/19] Testing Get All Products (GET /api/products)...")
    status, res = http_request("GET", "/api/products")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    products = res["data"]["products"]
    assert len(products) > 0, "No products returned"
    test_product = products[0]
    test_product_id = test_product["product_id"]
    second_product = products[1] if len(products) > 1 else products[0]
    second_product_id = second_product["product_id"]
    print(f" -> Passed (Status 200). Retrieved {len(products)} products from Atlas.")
    results["4. Get all products"] = "Working"

    # -------------------------------------------------------------
    # 5. Get a single product
    # -------------------------------------------------------------
    print(f"\n[Feature 5/19] Testing Get Single Product (GET /api/products/{test_product_id})...")
    status, res = http_request("GET", f"/api/products/{test_product_id}")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["name"] == test_product["name"]
    print(f" -> Passed (Status 200). Retrieved details for '{test_product['name']}'.")
    results["5. Get a single product"] = "Working"

    # -------------------------------------------------------------
    # 6. Search products
    # -------------------------------------------------------------
    print("\n[Feature 6/19] Testing Search Products (GET /api/products/search?q=Headphones)...")
    status, res = http_request("GET", "/api/products/search?q=Headphones")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    search_items = res["data"]["products"]
    assert len(search_items) >= 1
    print(f" -> Passed (Status 200). Search returned {len(search_items)} matching product(s).")
    results["6. Search products"] = "Working"

    # -------------------------------------------------------------
    # 7. Filter products by category
    # -------------------------------------------------------------
    print("\n[Feature 7/19] Testing Filter by Category (GET /api/products/category/Electronics)...")
    status, res = http_request("GET", "/api/products/category/Electronics")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    cat_items = res["data"]["products"]
    assert len(cat_items) >= 1
    assert all(item["category"] == "Electronics" for item in cat_items)
    print(f" -> Passed (Status 200). Retrieved {len(cat_items)} Electronics products.")
    results["7. Filter products by category"] = "Working"

    # -------------------------------------------------------------
    # 8. Add product to cart
    # -------------------------------------------------------------
    print(f"\n[Feature 8/19] Testing Add Product to Cart (POST /api/cart)...")
    status, res = http_request("POST", "/api/cart", {
        "user_id": user_id,
        "product_id": test_product_id,
        "quantity": 2
    })
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    cart_items = res["data"]["items"]
    assert len(cart_items) == 1
    assert cart_items[0]["quantity"] == 2

    # Verify directly in MongoDB Atlas 'carts' collection
    db_cart = carts_coll.find_one({"user_id": user_id})
    assert db_cart is not None, "Cart document not found in MongoDB Atlas"
    assert len(db_cart["items"]) == 1
    print(" -> Passed (Status 200). Item added and verified in Atlas 'carts' collection.")
    results["8. Add product to cart"] = "Working"

    # -------------------------------------------------------------
    # 9. Update cart quantity
    # -------------------------------------------------------------
    print(f"\n[Feature 9/19] Testing Update Cart Quantity (PUT /api/cart/{user_id}/{test_product_id})...")
    status, res = http_request("PUT", f"/api/cart/{user_id}/{test_product_id}", {
        "quantity": 3
    })
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["items"][0]["quantity"] == 3

    # Verify directly in Atlas
    db_cart = carts_coll.find_one({"user_id": user_id})
    assert db_cart["items"][0]["quantity"] == 3
    print(" -> Passed (Status 200). Cart quantity updated to 3 and verified in Atlas.")
    results["9. Update cart quantity"] = "Working"

    # -------------------------------------------------------------
    # 10. Remove product from cart
    # -------------------------------------------------------------
    print(f"\n[Feature 10/19] Testing Remove Product from Cart (DELETE /api/cart/{user_id}/...)...")
    # First add second product
    http_request("POST", "/api/cart", {
        "user_id": user_id,
        "product_id": second_product_id,
        "quantity": 1
    })
    # Remove second product
    status, res = http_request("DELETE", f"/api/cart/{user_id}/{second_product_id}")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert all(item["product_id"] != second_product_id for item in res["data"]["items"])

    # Verify in Atlas
    db_cart = carts_coll.find_one({"user_id": user_id})
    assert all(item["product_id"] != second_product_id for item in db_cart["items"])
    print(" -> Passed (Status 200). Product removed from cart and verified in Atlas.")
    results["10. Remove product from cart"] = "Working"

    # -------------------------------------------------------------
    # 11. View cart and calculate total
    # -------------------------------------------------------------
    print(f"\n[Feature 11/19] Testing View Cart & Total Calculation (GET /api/cart/{user_id})...")
    status, res = http_request("GET", f"/api/cart/{user_id}")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    cart_data = res["data"]
    expected_total = round(test_product["price"] * 3, 2)
    assert abs(cart_data["total_price"] - expected_total) < 0.01, f"Expected {expected_total}, got {cart_data['total_price']}"
    print(f" -> Passed (Status 200). Total price calculated correctly: ${cart_data['total_price']}.")
    results["11. View cart and calculate total"] = "Working"

    # -------------------------------------------------------------
    # 12. Create an order
    # -------------------------------------------------------------
    print("\n[Feature 12/19] Testing Create Order / Checkout (POST /api/orders)...")
    # Record initial stock before checkout
    init_stock_doc = products_coll.find_one({"$or": [{"_id": to_object_id(test_product_id)}, {"product_id": test_product_id}]})
    initial_stock = init_stock_doc["stock"]

    shipping_address = {
        "full_name": test_name,
        "street": "123 Academic Way, Apt 4B",
        "city": "University Heights",
        "state": "State",
        "postal_code": "54321",
        "phone": "555-987-6543"
    }
    status, res = http_request("POST", "/api/orders", {
        "user_id": user_id,
        "shipping_address": shipping_address
    })
    assert status == 201, f"Expected 201, got {status}: {res}"
    assert res.get("success") is True
    created_order = res["data"]
    created_order_id = created_order["order_id"]
    assert created_order["status"] == "Pending"

    # Verify in MongoDB Atlas 'orders' collection
    db_order = orders_coll.find_one({"order_id": created_order_id})
    assert db_order is not None, "Order document was not saved in Atlas 'orders' collection"
    assert db_order["total_amount"] == created_order["total_amount"]

    # Verify cart was cleared in Atlas
    db_cart = carts_coll.find_one({"user_id": user_id})
    assert len(db_cart.get("items", [])) == 0, "Cart was not cleared in Atlas after order placement"

    # Verify stock was decremented in Atlas
    updated_stock_doc = products_coll.find_one({"$or": [{"_id": to_object_id(test_product_id)}, {"product_id": test_product_id}]})
    assert updated_stock_doc["stock"] == initial_stock - 3, "Product stock was not decremented in Atlas"
    print(f" -> Passed (Status 201). Order '{created_order_id}' created; cart cleared; stock decremented in Atlas.")
    results["12. Create an order"] = "Working"

    # -------------------------------------------------------------
    # 13. View user order history
    # -------------------------------------------------------------
    print(f"\n[Feature 13/19] Testing User Order History (GET /api/orders/{user_id})...")
    status, res = http_request("GET", f"/api/orders/{user_id}")
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    user_orders = res["data"]["orders"]
    assert any(o["order_id"] == created_order_id for o in user_orders)

    # Test single order details
    status_single, res_single = http_request("GET", f"/api/orders/{user_id}/{created_order_id}")
    assert status_single == 200
    assert res_single["data"]["order_id"] == created_order_id
    print(f" -> Passed (Status 200). User order history & order details retrieved.")
    results["13. View user order history"] = "Working"

    # -------------------------------------------------------------
    # 14. Admin add product
    # -------------------------------------------------------------
    print("\n[Feature 14/19] Testing Admin Add Product (POST /api/admin/products)...")
    new_product_payload = {
        "name": "Smart LED Desk Glow",
        "description": "Adjustable color temperature LED bar with rhythm sync",
        "category": "Electronics",
        "price": 39.99,
        "image_url": "https://example.com/desk-light.jpg",
        "stock": 45,
        "rating": 4.9
    }
    status, res = http_request("POST", "/api/admin/products", new_product_payload, ADMIN_HEADERS)
    assert status == 201, f"Expected 201, got {status}: {res}"
    assert res.get("success") is True
    admin_prod_id = res["data"]["product_id"]

    # Verify directly in MongoDB Atlas
    db_prod = products_coll.find_one({"$or": [{"_id": to_object_id(admin_prod_id)}, {"product_id": admin_prod_id}]})
    assert db_prod is not None, "Added product not found in Atlas 'products' collection"
    assert db_prod["name"] == "Smart LED Desk Glow"
    print(f" -> Passed (Status 201). Product added and verified in Atlas.")
    results["14. Admin add product"] = "Working"

    # -------------------------------------------------------------
    # 15. Admin update product
    # -------------------------------------------------------------
    print(f"\n[Feature 15/19] Testing Admin Update Product (PUT /api/admin/products/{admin_prod_id})...")
    status, res = http_request("PUT", f"/api/admin/products/{admin_prod_id}", {
        "price": 34.99,
        "name": "Smart LED Desk Glow Pro"
    }, ADMIN_HEADERS)
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["price"] == 34.99

    # Verify in Atlas
    db_prod = products_coll.find_one({"$or": [{"_id": to_object_id(admin_prod_id)}, {"product_id": admin_prod_id}]})
    assert db_prod["price"] == 34.99
    assert db_prod["name"] == "Smart LED Desk Glow Pro"
    print(" -> Passed (Status 200). Product updated in Atlas.")
    results["15. Admin update product"] = "Working"

    # -------------------------------------------------------------
    # 16. Admin update stock
    # -------------------------------------------------------------
    print(f"\n[Feature 16/19] Testing Admin Update Stock (PATCH /api/admin/products/{admin_prod_id}/stock)...")
    status, res = http_request("PATCH", f"/api/admin/products/{admin_prod_id}/stock", {
        "stock": 75
    }, ADMIN_HEADERS)
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["stock"] == 75

    # Verify in Atlas
    db_prod = products_coll.find_one({"$or": [{"_id": to_object_id(admin_prod_id)}, {"product_id": admin_prod_id}]})
    assert db_prod["stock"] == 75
    print(" -> Passed (Status 200). Inventory stock updated to 75 in Atlas.")
    results["16. Admin update stock"] = "Working"

    # -------------------------------------------------------------
    # 17. Admin view orders
    # -------------------------------------------------------------
    print("\n[Feature 17/19] Testing Admin View Orders (GET /api/admin/orders)...")
    status, res = http_request("GET", "/api/admin/orders", headers=ADMIN_HEADERS)
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    all_admin_orders = res["data"]["orders"]
    assert len(all_admin_orders) >= 1
    assert any(o["order_id"] == created_order_id for o in all_admin_orders)
    print(f" -> Passed (Status 200). Retrieved {len(all_admin_orders)} customer orders.")
    results["17. Admin view orders"] = "Working"

    # -------------------------------------------------------------
    # 18. Admin update order status
    # -------------------------------------------------------------
    print(f"\n[Feature 18/19] Testing Admin Update Order Status (PATCH /api/admin/orders/{created_order_id}/status)...")
    status, res = http_request("PATCH", f"/api/admin/orders/{created_order_id}/status", {
        "status": "Confirmed"
    }, ADMIN_HEADERS)
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True
    assert res["data"]["status"] == "Confirmed"

    # Verify directly in MongoDB Atlas
    db_order = orders_coll.find_one({"order_id": created_order_id})
    assert db_order["status"] == "Confirmed", "Order status in Atlas was not updated to 'Confirmed'"
    print(" -> Passed (Status 200). Order status transitioned to 'Confirmed' in Atlas.")
    results["18. Admin update order status"] = "Working"

    # -------------------------------------------------------------
    # 19. Admin delete product
    # -------------------------------------------------------------
    print(f"\n[Feature 19/19] Testing Admin Delete Product (DELETE /api/admin/products/{admin_prod_id})...")
    status, res = http_request("DELETE", f"/api/admin/products/{admin_prod_id}", headers=ADMIN_HEADERS)
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("success") is True

    # Verify deletion in Atlas
    db_prod = products_coll.find_one({"$or": [{"_id": to_object_id(admin_prod_id)}, {"product_id": admin_prod_id}]})
    assert db_prod is None, "Deleted product was still found in Atlas"
    print(" -> Passed (Status 200). Product removed from Atlas.")
    results["19. Admin delete product"] = "Working"

    # Cleanup temporary test user and order from Atlas
    users_coll.delete_one({"_id": to_object_id(user_id)})
    carts_coll.delete_one({"user_id": user_id})
    orders_coll.delete_one({"order_id": created_order_id})
    print("\n[Cleanup] Test documents cleaned up cleanly from Atlas.")

    print("\n" + "=" * 70)
    print("  ALL 19 ENDPOINTS TESTED SUCCESSFULLY AGAINST LIVE MONGODB ATLAS!")
    print("=" * 70)
    for k, v in results.items():
        print(f"  [OK] {k:<40} : {v}")

    return True


if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        sys.exit(1)
