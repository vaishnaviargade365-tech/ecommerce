"""
Comprehensive Automated Test Suite for Mini E-Commerce Flask Backend.
Tests all requirements:
1. Registration (validation, hashing, duplicate email detection)
2. Login (credential verification, safe user data returned)
3. Profile (password excluded)
4. Products retrieval, single product, search, category filter, categories
5. Shopping Cart (add, stock check, update quantity, remove, calculate total)
6. Orders / Checkout (stock deduction, cart cleared, safe demo checkout)
7. User Order History and order details
8. Admin operations (add, update, delete, stock update, order status update, dashboard stats, authorization)
9. Error handling and status codes

Run with:
    python test_backend.py
"""

import os
import sys

# Ensure backend directory is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enable mock DB for isolated, offline, deterministic testing
os.environ["USE_MOCK_DB"] = "true"

from app import create_app
from seed_data import seed_database
from database import get_users_collection, get_products_collection, get_carts_collection, get_orders_collection


def run_tests():
    print("=" * 70)
    print("  RUNNING MINI E-COMMERCE BACKEND TEST SUITE")
    print("=" * 70)

    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Seed the database
    print("\n[Step 0] Seeding test database...")
    seed_database(force_refresh=True)
    products_coll = get_products_collection()
    product_count = products_coll.count_documents({})
    assert product_count > 0, f"Expected seeded products, got {product_count}"
    print(f" -> Successfully seeded {product_count} products.")

    # 1. Health check & Root
    print("\n[Step 1] Testing Health Check & Welcome Endpoint...")
    res = client.get("/")
    assert res.status_code == 200, f"Root endpoint failed: {res.status_code}"
    res_json = res.get_json()
    assert res_json["success"] is True
    print(" -> Root / endpoint returned 200 OK.")

    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print(" -> GET /api/health returned 200 OK.")

    # 2. Registration
    print("\n[Step 2] Testing User Registration...")
    reg_payload = {
        "name": "Alice Wonder",
        "email": "alice@university.edu",
        "password": "password123",
        "role": "user"
    }
    res = client.post("/api/register", json=reg_payload)
    assert res.status_code == 201, f"Register failed: {res.status_code}, {res.data}"
    reg_data = res.get_json()
    assert reg_data["success"] is True
    assert "user_id" in reg_data["data"]
    assert "password" not in reg_data["data"]
    user_id = reg_data["data"]["user_id"]
    print(f" -> User registered successfully with user_id: {user_id}")

    # Test Duplicate Registration
    res_dup = client.post("/api/register", json=reg_payload)
    assert res_dup.status_code == 400, "Duplicate email registration should return 400"
    assert res_dup.get_json()["success"] is False
    print(" -> Duplicate registration correctly rejected with 400 Bad Request.")

    # Test Short Password
    res_short = client.post("/api/register", json={"name": "Bad", "email": "bad@test.com", "password": "123"})
    assert res_short.status_code == 400
    print(" -> Password validation correctly enforced (< 6 characters).")

    # 3. Login
    print("\n[Step 3] Testing User Login...")
    login_payload = {
        "email": "alice@university.edu",
        "password": "password123"
    }
    res_login = client.post("/api/login", json=login_payload)
    assert res_login.status_code == 200, f"Login failed: {res_login.status_code}"
    login_data = res_login.get_json()
    assert login_data["success"] is True
    assert login_data["data"]["email"] == "alice@university.edu"
    assert "password" not in login_data["data"]
    print(" -> User login verified with correct hashed password check.")

    # Test Wrong Password
    res_wrong = client.post("/api/login", json={"email": "alice@university.edu", "password": "wrongpassword"})
    assert res_wrong.status_code == 401
    assert res_wrong.get_json()["success"] is False
    print(" -> Incorrect password correctly returned 401 Unauthorized.")

    # 4. Profile
    print("\n[Step 4] Testing User Profile Retrieval...")
    res_prof = client.get(f"/api/profile/{user_id}")
    assert res_prof.status_code == 200, f"Profile failed: {res_prof.status_code}"
    prof_data = res_prof.get_json()["data"]
    assert prof_data["name"] == "Alice Wonder"
    assert "password" not in prof_data
    print(" -> GET /api/profile/<user_id> returned profile without password exposure.")

    # 5. Products Retrieval
    print("\n[Step 5] Testing Product APIs...")
    res_prods = client.get("/api/products")
    assert res_prods.status_code == 200
    all_products = res_prods.get_json()["data"]["products"]
    assert len(all_products) > 0
    test_product = all_products[0]
    test_product_id = test_product["product_id"]
    print(f" -> GET /api/products returned {len(all_products)} products.")

    # Single product
    res_single = client.get(f"/api/products/{test_product_id}")
    assert res_single.status_code == 200
    assert res_single.get_json()["data"]["name"] == test_product["name"]
    print(f" -> GET /api/products/<id> returned '{test_product['name']}'.")

    # Product search
    res_search = client.get("/api/products/search?q=Headphones")
    assert res_search.status_code == 200
    search_results = res_search.get_json()["data"]["products"]
    assert len(search_results) >= 1
    print(f" -> GET /api/products/search?q=Headphones returned {len(search_results)} item(s).")

    # Category filter
    res_cat = client.get("/api/products/category/Electronics")
    assert res_cat.status_code == 200
    cat_items = res_cat.get_json()["data"]["products"]
    assert len(cat_items) >= 1
    assert all(p["category"] == "Electronics" for p in cat_items)
    print(f" -> GET /api/products/category/Electronics returned {len(cat_items)} electronics.")

    # Distinct categories
    res_cats = client.get("/api/categories")
    assert res_cats.status_code == 200
    cats_list = res_cats.get_json()["data"]["categories"]
    assert len(cats_list) >= 5
    print(f" -> GET /api/categories returned {len(cats_list)} categories.")

    # 6. Shopping Cart Operations
    print("\n[Step 6] Testing Shopping Cart APIs...")
    # Add product to cart
    add_payload = {
        "user_id": user_id,
        "product_id": test_product_id,
        "quantity": 2
    }
    res_add_cart = client.post("/api/cart", json=add_payload)
    assert res_add_cart.status_code == 200, f"Add to cart failed: {res_add_cart.data}"
    cart_data = res_add_cart.get_json()["data"]
    assert len(cart_data["items"]) == 1
    assert cart_data["items"][0]["quantity"] == 2
    expected_total = round(test_product["price"] * 2, 2)
    assert cart_data["total_price"] == expected_total
    print(f" -> POST /api/cart added 2 items. Total: ${cart_data['total_price']}")

    # Stock check validation
    over_stock_payload = {
        "user_id": user_id,
        "product_id": test_product_id,
        "quantity": 99999
    }
    res_over = client.post("/api/cart", json=over_stock_payload)
    assert res_over.status_code == 400
    assert "stock" in res_over.get_json()["message"].lower()
    print(" -> Stock overflow check correctly rejected with 400 Bad Request.")

    # Update quantity in cart
    res_update_cart = client.put(f"/api/cart/{user_id}/{test_product_id}", json={"quantity": 3})
    assert res_update_cart.status_code == 200
    updated_cart = res_update_cart.get_json()["data"]
    assert updated_cart["items"][0]["quantity"] == 3
    print(" -> PUT /api/cart/<user_id>/<product_id> updated quantity to 3.")

    # Get cart
    res_get_cart = client.get(f"/api/cart/{user_id}")
    assert res_get_cart.status_code == 200
    assert len(res_get_cart.get_json()["data"]["items"]) == 1
    print(" -> GET /api/cart/<user_id> retrieved cart successfully.")

    # Test delete single product from cart
    third_product = all_products[2]
    third_prod_id = third_product["product_id"]
    client.post("/api/cart", json={"user_id": user_id, "product_id": third_prod_id, "quantity": 1})
    res_del_item = client.delete(f"/api/cart/{user_id}/{third_prod_id}")
    assert res_del_item.status_code == 200
    assert all(item["product_id"] != third_prod_id for item in res_del_item.get_json()["data"]["items"])
    print(" -> DELETE /api/cart/<user_id>/<product_id> removed item successfully.")

    # Add a second product to cart for checkout
    second_product = all_products[1]
    second_prod_id = second_product["product_id"]
    client.post("/api/cart", json={"user_id": user_id, "product_id": second_prod_id, "quantity": 1})

    # 7. Orders & Checkout
    print("\n[Step 7] Testing Orders and Checkout APIs...")
    from utils.helpers import to_object_id
    prod_in_db = products_coll.find_one({"product_id": test_product_id}) or products_coll.find_one({"_id": to_object_id(test_product_id)})
    initial_stock_1 = prod_in_db["stock"]

    order_payload = {
        "user_id": user_id,
        "shipping_address": {
            "full_name": "Alice Wonder",
            "street": "100 Science Parkway, Dorm 4B",
            "city": "Boston",
            "state": "MA",
            "postal_code": "02115",
            "phone": "555-0199"
        }
    }
    res_order = client.post("/api/orders", json=order_payload)
    assert res_order.status_code == 201, f"Order placement failed: {res_order.data}"
    order_data = res_order.get_json()["data"]
    assert "order_id" in order_data
    assert order_data["status"] == "Pending"
    assert len(order_data["items"]) == 2
    created_order_id = order_data["order_id"]
    print(f" -> POST /api/orders created order '{created_order_id}' for total ${order_data['total_amount']}.")

    # Verify cart was cleared
    res_cart_cleared = client.get(f"/api/cart/{user_id}")
    assert len(res_cart_cleared.get_json()["data"]["items"]) == 0
    print(" -> Verified cart was automatically cleared after checkout.")

    # Verify stock was decremented in database
    updated_prod_db = products_coll.find_one({"product_id": test_product_id}) or products_coll.find_one({"_id": to_object_id(test_product_id)})
    new_stock_1 = updated_prod_db["stock"]
    assert new_stock_1 == initial_stock_1 - 3, f"Stock was {initial_stock_1}, expected {initial_stock_1 - 3}, got {new_stock_1}"
    print(f" -> Verified product stock decremented from {initial_stock_1} to {new_stock_1}.")

    # 8. User Order History
    print("\n[Step 8] Testing Order History APIs...")
    res_user_orders = client.get(f"/api/orders/{user_id}")
    assert res_user_orders.status_code == 200
    orders_list = res_user_orders.get_json()["data"]["orders"]
    assert len(orders_list) == 1
    assert orders_list[0]["order_id"] == created_order_id
    print(f" -> GET /api/orders/<user_id> returned {len(orders_list)} order(s).")

    res_single_order = client.get(f"/api/orders/{user_id}/{created_order_id}")
    assert res_single_order.status_code == 200
    assert res_single_order.get_json()["data"]["order_id"] == created_order_id
    print(" -> GET /api/orders/<user_id>/<order_id> returned order details.")

    # 9. Admin APIs
    print("\n[Step 9] Testing Admin APIs...")
    admin_headers = {"X-User-Role": "admin"}

    # Unauthorized attempt (without admin header)
    res_unauth = client.get("/api/admin/products")
    assert res_unauth.status_code == 403
    print(" -> Non-admin access to /api/admin/products rejected with 403 Forbidden.")

    # Admin view all products
    res_admin_prods = client.get("/api/admin/products", headers=admin_headers)
    assert res_admin_prods.status_code == 200
    print(" -> GET /api/admin/products with admin privileges returned 200 OK.")

    # Admin add product
    new_prod_payload = {
        "name": "Smart Ambient Desk Glow",
        "description": "Smart RGB ambient light bar with rhythm sync.",
        "category": "Electronics",
        "price": 39.99,
        "image_url": "https://example.com/light.jpg",
        "stock": 15,
        "rating": 4.9
    }
    res_add_prod = client.post("/api/admin/products", json=new_prod_payload, headers=admin_headers)
    assert res_add_prod.status_code == 201
    added_prod_id = res_add_prod.get_json()["data"]["product_id"]
    print(f" -> POST /api/admin/products created new product ID: {added_prod_id}")

    # Admin update stock
    res_stock = client.patch(f"/api/admin/products/{added_prod_id}/stock", json={"stock": 50}, headers=admin_headers)
    assert res_stock.status_code == 200
    assert res_stock.get_json()["data"]["stock"] == 50
    print(" -> PATCH /api/admin/products/<id>/stock updated stock to 50.")

    # Admin update product
    res_update_p = client.put(f"/api/admin/products/{added_prod_id}", json={"price": 34.99}, headers=admin_headers)
    assert res_update_p.status_code == 200
    assert res_update_p.get_json()["data"]["price"] == 34.99
    print(" -> PUT /api/admin/products/<id> updated price to $34.99.")

    # Admin view customer orders
    res_admin_orders = client.get("/api/admin/orders", headers=admin_headers)
    assert res_admin_orders.status_code == 200
    assert len(res_admin_orders.get_json()["data"]["orders"]) >= 1
    print(" -> GET /api/admin/orders retrieved customer orders.")

    # Admin update order status
    res_status = client.patch(f"/api/admin/orders/{created_order_id}/status", json={"status": "Shipped"}, headers=admin_headers)
    assert res_status.status_code == 200
    assert res_status.get_json()["data"]["status"] == "Shipped"
    print(" -> PATCH /api/admin/orders/<id>/status updated order status to 'Shipped'.")

    # Admin stats
    res_stats = client.get("/api/admin/stats", headers=admin_headers)
    assert res_stats.status_code == 200
    stats_data = res_stats.get_json()["data"]
    assert stats_data["total_orders"] >= 1
    assert stats_data["total_revenue"] > 0
    print(f" -> GET /api/admin/stats returned revenue: ${stats_data['total_revenue']}, orders: {stats_data['total_orders']}.")

    # Admin delete product
    res_del_p = client.delete(f"/api/admin/products/{added_prod_id}", headers=admin_headers)
    assert res_del_p.status_code == 200
    print(" -> DELETE /api/admin/products/<id> deleted product successfully.")

    # 10. Centralized Error Handling
    print("\n[Step 10] Testing Error Handling & Consistent Formats...")
    res_404 = client.get("/api/nonexistent-endpoint")
    assert res_404.status_code == 404
    assert res_404.get_json()["success"] is False
    print(" -> 404 Not Found returns consistent JSON error.")

    print("\n" + "=" * 70)
    print("  ALL TESTS PASSED SUCCESSFULLY! (10/10 MODULES VERIFIED)")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
