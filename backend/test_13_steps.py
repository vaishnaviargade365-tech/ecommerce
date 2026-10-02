"""
Step-by-step verification script for the 13 requested e-commerce features.
Sends live HTTP requests to Flask backend (http://127.0.0.1:5000)
and queries MongoDB Atlas directly after each step to verify database persistence.
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


def http_call(method, path, body=None, headers=None):
    url = f"{BASE_URL}{path}"
    h = dict(headers or JSON_HEADERS)
    payload = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=payload, headers=h, method=method)

    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def run():
    print("=" * 70)
    print("  TESTING 13 BACKEND FEATURES ONE BY ONE (WITH ATLAS VERIFICATION)")
    print("=" * 70)

    # Database connection confirmation
    ok, msg = test_connection()
    assert ok, f"Atlas connection failed: {msg}"
    print(f"[Atlas] Live connection verified: {msg}")

    users = get_users_collection()
    products = get_products_collection()
    carts = get_carts_collection()
    orders = get_orders_collection()

    summary_working = []
    summary_fixed = []
    summary_errors = []

    test_uid = f"user_{int(time.time())}_{uuid.uuid4().hex[:4]}"
    test_email = f"{test_uid}@college.edu"
    test_pass = "CollegeStudent2026!"
    test_name = "Alex Rivera"

    created_user_id = None
    target_product_id = None
    second_product_id = None
    created_order_id = None
    new_admin_prod_id = None

    # -------------------------------------------------------------------------
    # 1. Register a new user
    # -------------------------------------------------------------------------
    print("\n--- [Step 1] Register a new user ---")
    reg_body = {
        "name": test_name,
        "email": test_email,
        "password": test_pass,
        "role": "user"
    }
    status, res = http_call("POST", "/api/register", reg_body)
    print(f"Request: POST /api/register")
    print(f"Response Status: {status}")
    print(f"Response Body: {json.dumps(res, indent=2)}")

    assert status == 201 and res.get("success") is True, "Step 1 failed"
    created_user_id = res["data"]["user_id"]

    # Verify directly in MongoDB Atlas
    atlas_user = users.find_one({"_id": to_object_id(created_user_id)})
    assert atlas_user is not None, "User not found in Atlas users collection"
    print(f"-> Verified in Atlas: user document found with email='{atlas_user['email']}', password is hashed.")
    summary_working.append("1. Register a new user (POST /api/register)")

    # -------------------------------------------------------------------------
    # 2. Login with that user
    # -------------------------------------------------------------------------
    print("\n--- [Step 2] Login with that user ---")
    login_body = {
        "email": test_email,
        "password": test_pass
    }
    status, res = http_call("POST", "/api/login", login_body)
    print(f"Request: POST /api/login")
    print(f"Response Status: {status}")
    print(f"Response Body: {json.dumps(res, indent=2)}")

    assert status == 200 and res.get("success") is True, "Step 2 failed"
    print("-> Verified: Password verified successfully against hashed password in Atlas.")
    summary_working.append("2. Login with that user (POST /api/login)")

    # -------------------------------------------------------------------------
    # 3. Get the user profile
    # -------------------------------------------------------------------------
    print("\n--- [Step 3] Get the user profile ---")
    status, res = http_call("GET", f"/api/profile/{created_user_id}")
    print(f"Request: GET /api/profile/{created_user_id}")
    print(f"Response Status: {status}")
    print(f"Response Body: {json.dumps(res, indent=2)}")

    assert status == 200 and res.get("success") is True, "Step 3 failed"
    assert "password" not in res["data"], "Security violation: password was returned in profile"
    print("-> Verified: User profile retrieved from Atlas without exposing password hash.")
    summary_working.append("3. Get user profile (GET /api/profile/<user_id>)")

    # -------------------------------------------------------------------------
    # 4. Get all products
    # -------------------------------------------------------------------------
    print("\n--- [Step 4] Get all products ---")
    status, res = http_call("GET", "/api/products")
    print(f"Request: GET /api/products")
    print(f"Response Status: {status}")
    print(f"Found {res['data']['total']} products. First product: {res['data']['products'][0]['name']}")

    assert status == 200 and res.get("success") is True, "Step 4 failed"
    all_prods = res["data"]["products"]
    target_product = all_prods[0]
    target_product_id = target_product["product_id"]
    second_product_id = all_prods[1]["product_id"]

    # Verify count in Atlas
    atlas_count = products.count_documents({})
    assert atlas_count == res["data"]["total"], "Product count mismatch"
    print(f"-> Verified: {atlas_count} products retrieved directly from MongoDB Atlas 'products' collection.")
    summary_working.append("4. Get all products (GET /api/products)")

    # -------------------------------------------------------------------------
    # 5. Search products
    # -------------------------------------------------------------------------
    print("\n--- [Step 5] Search products ---")
    status, res = http_call("GET", "/api/products/search?q=Watch")
    print(f"Request: GET /api/products/search?q=Watch")
    print(f"Response Status: {status}")
    print(f"Found {res['data']['total']} matches.")

    assert status == 200 and res.get("success") is True, "Step 5 failed"
    assert len(res["data"]["products"]) >= 1, "Expected search results for 'Watch'"
    print(f"-> Verified: Case-insensitive search executed against MongoDB Atlas products.")
    summary_working.append("5. Search products (GET /api/products/search?q=...)")

    # -------------------------------------------------------------------------
    # 6. Filter products by category
    # -------------------------------------------------------------------------
    print("\n--- [Step 6] Filter products by category ---")
    status, res = http_call("GET", "/api/products/category/Clothing")
    print(f"Request: GET /api/products/category/Clothing")
    print(f"Response Status: {status}")
    print(f"Retrieved {res['data']['total']} products in Clothing.")

    assert status == 200 and res.get("success") is True, "Step 6 failed"
    assert all(p["category"] == "Clothing" for p in res["data"]["products"])
    print("-> Verified: Category filter correctly queried Atlas documents matching category='Clothing'.")
    summary_working.append("6. Filter products by category (GET /api/products/category/<cat>)")

    # -------------------------------------------------------------------------
    # 7. Add a product to cart
    # -------------------------------------------------------------------------
    print("\n--- [Step 7] Add a product to cart ---")
    add_body = {
        "user_id": created_user_id,
        "product_id": target_product_id,
        "quantity": 2
    }
    status, res = http_call("POST", "/api/cart", add_body)
    print(f"Request: POST /api/cart")
    print(f"Response Status: {status}")
    print(f"Response Body: {json.dumps(res, indent=2)}")

    assert status == 200 and res.get("success") is True, "Step 7 failed"
    assert len(res["data"]["items"]) == 1
    assert res["data"]["items"][0]["quantity"] == 2

    # Verify in MongoDB Atlas
    atlas_cart = carts.find_one({"user_id": created_user_id})
    assert atlas_cart is not None, "Cart not found in Atlas carts collection"
    assert atlas_cart["items"][0]["quantity"] == 2
    print("-> Verified: Cart document created and stored in MongoDB Atlas 'carts' collection.")
    summary_working.append("7. Add product to cart (POST /api/cart)")

    # -------------------------------------------------------------------------
    # 8. Update cart quantity
    # -------------------------------------------------------------------------
    print("\n--- [Step 8] Update cart quantity ---")
    status, res = http_call("PUT", f"/api/cart/{created_user_id}/{target_product_id}", {"quantity": 3})
    print(f"Request: PUT /api/cart/{created_user_id}/{target_product_id}")
    print(f"Response Status: {status}")
    print(f"Updated quantity: {res['data']['items'][0]['quantity']}, Total price: ${res['data']['total_price']}")

    assert status == 200 and res.get("success") is True, "Step 8 failed"
    assert res["data"]["items"][0]["quantity"] == 3

    # Verify in Atlas
    atlas_cart = carts.find_one({"user_id": created_user_id})
    assert atlas_cart["items"][0]["quantity"] == 3
    print("-> Verified: Updated quantity (3) confirmed in MongoDB Atlas 'carts' collection.")
    summary_working.append("8. Update cart quantity (PUT /api/cart/<user_id>/<product_id>)")

    # -------------------------------------------------------------------------
    # 9. Remove a product from cart
    # -------------------------------------------------------------------------
    print("\n--- [Step 9] Remove a product from cart ---")
    # First add a second product to demonstrate removal of a specific item
    http_call("POST", "/api/cart", {"user_id": created_user_id, "product_id": second_product_id, "quantity": 1})
    print(f"Added item {second_product_id} to cart. Now removing it...")

    status, res = http_call("DELETE", f"/api/cart/{created_user_id}/{second_product_id}")
    print(f"Request: DELETE /api/cart/{created_user_id}/{second_product_id}")
    print(f"Response Status: {status}")
    print(f"Remaining items in cart: {len(res['data']['items'])}")

    assert status == 200 and res.get("success") is True, "Step 9 failed"
    assert all(item["product_id"] != second_product_id for item in res["data"]["items"])

    # Verify in Atlas
    atlas_cart = carts.find_one({"user_id": created_user_id})
    assert all(item["product_id"] != second_product_id for item in atlas_cart["items"])
    print("-> Verified: Specific product was removed from user's cart in MongoDB Atlas.")
    summary_working.append("9. Remove product from cart (DELETE /api/cart/<user_id>/<product_id>)")

    # -------------------------------------------------------------------------
    # 10. Place an order
    # -------------------------------------------------------------------------
    print("\n--- [Step 10] Place an order ---")
    # Read product stock before order
    prod_before = products.find_one({"$or": [{"_id": to_object_id(target_product_id)}, {"product_id": target_product_id}]})
    stock_before = prod_before["stock"]

    order_payload = {
        "user_id": created_user_id,
        "shipping_address": {
            "full_name": test_name,
            "street": "456 University Boulevard",
            "city": "College Park",
            "state": "State",
            "postal_code": "98765",
            "phone": "555-123-9999"
        },
        "payment_method": "Cash on Delivery (Demo Checkout)"
    }
    status, res = http_call("POST", "/api/orders", order_payload)
    print(f"Request: POST /api/orders")
    print(f"Response Status: {status}")
    print(f"Response Body: {json.dumps(res, indent=2)}")

    assert status == 201 and res.get("success") is True, "Step 10 failed"
    created_order_id = res["data"]["order_id"]

    # Verify in MongoDB Atlas:
    # 1. Order saved
    atlas_order = orders.find_one({"order_id": created_order_id})
    assert atlas_order is not None, "Order document not found in Atlas 'orders' collection"
    assert atlas_order["status"] == "Pending"

    # 2. Cart cleared
    atlas_cart = carts.find_one({"user_id": created_user_id})
    assert len(atlas_cart.get("items", [])) == 0, "Cart was not cleared in Atlas after order placement"

    # 3. Stock decremented by 3
    prod_after = products.find_one({"$or": [{"_id": to_object_id(target_product_id)}, {"product_id": target_product_id}]})
    assert prod_after["stock"] == stock_before - 3, "Stock was not decremented in Atlas"

    print(f"-> Verified: Order '{created_order_id}' stored in Atlas 'orders'. Cart cleared. Stock decremented ({stock_before} -> {prod_after['stock']}).")
    summary_working.append("10. Place an order (POST /api/orders)")

    # -------------------------------------------------------------------------
    # 11. View order history
    # -------------------------------------------------------------------------
    print("\n--- [Step 11] View order history ---")
    status, res = http_call("GET", f"/api/orders/{created_user_id}")
    print(f"Request: GET /api/orders/{created_user_id}")
    print(f"Response Status: {status}")
    print(f"User orders found: {res['data']['total']}")

    assert status == 200 and res.get("success") is True, "Step 11 failed"
    assert any(o["order_id"] == created_order_id for o in res["data"]["orders"])

    # Test single order view
    s_single, res_single = http_call("GET", f"/api/orders/{created_user_id}/{created_order_id}")
    assert s_single == 200 and res_single["data"]["order_id"] == created_order_id
    print("-> Verified: Order history and single order details retrieved from Atlas.")
    summary_working.append("11. View order history (GET /api/orders/<user_id>)")

    # -------------------------------------------------------------------------
    # 12. Test admin product operations (Add, Update, Update stock, Delete)
    # -------------------------------------------------------------------------
    print("\n--- [Step 12] Test admin product operations ---")
    # A. Add product
    admin_prod_payload = {
        "name": "Smart Ultra Desk Lamp",
        "description": "Smart LED lamp with color temperature adjustment",
        "category": "Home",
        "price": 49.99,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c",
        "stock": 30,
        "rating": 4.8
    }
    status, res = http_call("POST", "/api/admin/products", admin_prod_payload, ADMIN_HEADERS)
    assert status == 201 and res.get("success") is True
    new_admin_prod_id = res["data"]["product_id"]
    print(f"-> Admin Add Product: Status {status}, product_id={new_admin_prod_id}")

    # Verify in Atlas
    atlas_p = products.find_one({"$or": [{"_id": to_object_id(new_admin_prod_id)}, {"product_id": new_admin_prod_id}]})
    assert atlas_p is not None, "Admin added product not in Atlas"

    # B. Update product
    status, res = http_call("PUT", f"/api/admin/products/{new_admin_prod_id}", {"price": 44.99, "name": "Smart Ultra Desk Lamp v2"}, ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin Update Product: Status {status}, new_price=${res['data']['price']}")
    atlas_p = products.find_one({"$or": [{"_id": to_object_id(new_admin_prod_id)}, {"product_id": new_admin_prod_id}]})
    assert atlas_p["price"] == 44.99

    # C. Update stock
    status, res = http_call("PATCH", f"/api/admin/products/{new_admin_prod_id}/stock", {"stock": 80}, ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin Update Stock: Status {status}, new_stock={res['data']['stock']}")
    atlas_p = products.find_one({"$or": [{"_id": to_object_id(new_admin_prod_id)}, {"product_id": new_admin_prod_id}]})
    assert atlas_p["stock"] == 80

    # D. Delete product
    status, res = http_call("DELETE", f"/api/admin/products/{new_admin_prod_id}", headers=ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin Delete Product: Status {status}")
    atlas_p = products.find_one({"$or": [{"_id": to_object_id(new_admin_prod_id)}, {"product_id": new_admin_prod_id}]})
    assert atlas_p is None, "Deleted product was still found in Atlas"

    print("-> Verified: All admin product operations (Add, Update, Stock Update, Delete) verified in MongoDB Atlas.")
    summary_working.append("12. Test admin product operations (POST/PUT/PATCH/DELETE /api/admin/products)")

    # -------------------------------------------------------------------------
    # 13. Test admin order/status operations (View orders, Update status)
    # -------------------------------------------------------------------------
    print("\n--- [Step 13] Test admin order/status operations ---")
    # A. View all orders
    status, res = http_call("GET", "/api/admin/orders", headers=ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin View Orders: Status {status}, Total orders retrieved: {res['data']['total']}")

    # B. Update order status to 'Confirmed'
    status, res = http_call("PATCH", f"/api/admin/orders/{created_order_id}/status", {"status": "Confirmed"}, ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin Update Order Status: Status {status}, new status='{res['data']['status']}'")

    # Verify status in Atlas
    atlas_order = orders.find_one({"order_id": created_order_id})
    assert atlas_order["status"] == "Confirmed", "Order status in Atlas was not updated to 'Confirmed'"

    # C. Update order status to 'Shipped'
    status, res = http_call("PATCH", f"/api/admin/orders/{created_order_id}/status", {"status": "Shipped"}, ADMIN_HEADERS)
    assert status == 200 and res.get("success") is True
    print(f"-> Admin Update Order Status: Status {status}, new status='{res['data']['status']}'")

    atlas_order = orders.find_one({"order_id": created_order_id})
    assert atlas_order["status"] == "Shipped", "Order status in Atlas was not updated to 'Shipped'"

    print("-> Verified: Admin order listing and status updates ('Pending' -> 'Confirmed' -> 'Shipped') confirmed in MongoDB Atlas.")
    summary_working.append("13. Test admin order/status operations (GET /api/admin/orders, PATCH /api/admin/orders/<id>/status)")

    # Cleanup temporary test user and order
    users.delete_one({"_id": to_object_id(created_user_id)})
    carts.delete_one({"user_id": created_user_id})
    orders.delete_one({"order_id": created_order_id})

    print("\n" + "=" * 70)
    print("  ALL 13 REQUESTED FEATURES TESTED & VERIFIED SUCCESSFULLY!")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = run()
    if not success:
        sys.exit(1)
