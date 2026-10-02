"""
Seed data script to populate MongoDB with realistic sample products and demo accounts.
Categories:
- Electronics
- Clothing
- Beauty
- Home
- Accessories

Can be run directly:
    python seed_data.py
Or called programmatically via seed_database().
"""

from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from database import (
    get_users_collection,
    get_products_collection,
    get_carts_collection,
    get_orders_collection,
    test_connection
)

SAMPLE_PRODUCTS = [
    # Electronics
    {
        "name": "Wireless Noise-Cancelling Headphones",
        "description": "Premium over-ear wireless headphones with active noise cancellation, 40-hour battery life, and crystal-clear audio.",
        "category": "Electronics",
        "price": 89.99,
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "stock": 25,
        "rating": 4.8
    },
    {
        "name": "Smart Fitness Watch v2",
        "description": "Waterproof smartwatch with continuous heart rate monitoring, sleep tracking, GPS navigation, and 7-day battery standby.",
        "category": "Electronics",
        "price": 59.99,
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "stock": 40,
        "rating": 4.6
    },
    {
        "name": "Portable Bluetooth Speaker",
        "description": "Compact 360-degree surround sound speaker with punchy bass, IPX7 water resistance, and 16 hours of continuous playtime.",
        "category": "Electronics",
        "price": 34.99,
        "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=600&auto=format&fit=crop&q=80",
        "stock": 30,
        "rating": 4.5
    },
    {
        "name": "Ergonomic Mechanical Keyboard",
        "description": "Tactile RGB backlit mechanical keyboard with hot-swappable switches, sound-dampening foam, and wrist rest.",
        "category": "Electronics",
        "price": 74.99,
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&auto=format&fit=crop&q=80",
        "stock": 18,
        "rating": 4.7
    },

    # Clothing
    {
        "name": "Classic Organic Cotton Crewneck T-Shirt",
        "description": "100% breathable organic combed cotton t-shirt with durable double stitching and a relaxed, comfortable modern fit.",
        "category": "Clothing",
        "price": 19.99,
        "image_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600&auto=format&fit=crop&q=80",
        "stock": 60,
        "rating": 4.6
    },
    {
        "name": "Vintage Washed Denim Jacket",
        "description": "Timeless unisex denim jacket crafted with premium heavy-wash cotton denim and metallic button detailing.",
        "category": "Clothing",
        "price": 54.99,
        "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600&auto=format&fit=crop&q=80",
        "stock": 22,
        "rating": 4.7
    },
    {
        "name": "Athletic Breathable Joggers",
        "description": "Lightweight stretch-fleece joggers with deep zippered pockets and an adjustable elastic drawstring waistband.",
        "category": "Clothing",
        "price": 32.50,
        "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=600&auto=format&fit=crop&q=80",
        "stock": 35,
        "rating": 4.4
    },
    {
        "name": "Cozy Oversized Fleece Hoodie",
        "description": "Ultra-soft brushed fleece pullover hoodie featuring kangaroo front pocket and ribbed cuffs for chilly days.",
        "category": "Clothing",
        "price": 42.00,
        "image_url": "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=600&auto=format&fit=crop&q=80",
        "stock": 28,
        "rating": 4.9
    },

    # Beauty
    {
        "name": "Hydrating Gentle Facial Cleanser",
        "description": "Dermatologist-tested foaming face wash infused with hyaluronic acid, ceramides, and soothing green tea extract.",
        "category": "Beauty",
        "price": 16.99,
        "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&auto=format&fit=crop&q=80",
        "stock": 45,
        "rating": 4.7
    },
    {
        "name": "Vitamin C Brightening Serum (30ml)",
        "description": "Antioxidant facial serum with 15% pure Vitamin C and ferulic acid to fade dark spots and boost natural radiance.",
        "category": "Beauty",
        "price": 24.50,
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&auto=format&fit=crop&q=80",
        "stock": 30,
        "rating": 4.8
    },
    {
        "name": "Nourishing Organic Argan Hair Oil",
        "description": "Pure Moroccan cold-pressed argan oil for heat protection, frizz control, split-end repair, and healthy shine.",
        "category": "Beauty",
        "price": 18.00,
        "image_url": "https://images.unsplash.com/photo-1608248597359-07e868ecb472?w=600&auto=format&fit=crop&q=80",
        "stock": 25,
        "rating": 4.5
    },

    # Home
    {
        "name": "Minimalist Ceramic Table Lamp",
        "description": "Warm ambient LED desk lamp with dimmable touch control, textured ceramic base, and natural linen shade.",
        "category": "Home",
        "price": 38.99,
        "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&auto=format&fit=crop&q=80",
        "stock": 20,
        "rating": 4.6
    },
    {
        "name": "Stainless Steel Insulated Thermal Flask (750ml)",
        "description": "Double-wall vacuum insulated water bottle keeping cold drinks chilled for 24h and hot beverages warm for 12h.",
        "category": "Home",
        "price": 21.99,
        "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80",
        "stock": 50,
        "rating": 4.8
    },
    {
        "name": "Ultrasonic Aromatherapy Oil Diffuser",
        "description": "Whisper-quiet 400ml essential oil diffuser with 7 ambient mood light colors and automatic safety shut-off.",
        "category": "Home",
        "price": 27.50,
        "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=600&auto=format&fit=crop&q=80",
        "stock": 35,
        "rating": 4.7
    },

    # Accessories
    {
        "name": "Genuine Leather Slim Bi-fold Wallet",
        "description": "Handcrafted top-grain leather wallet with RFID-blocking technology, 8 card slots, and dual currency compartments.",
        "category": "Accessories",
        "price": 29.99,
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&auto=format&fit=crop&q=80",
        "stock": 40,
        "rating": 4.7
    },
    {
        "name": "Polarized UV400 Wayfarer Sunglasses",
        "description": "Classic unisex polarized sunglasses with scratch-resistant lenses, glare reduction, and durable acetate frames.",
        "category": "Accessories",
        "price": 26.00,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&auto=format&fit=crop&q=80",
        "stock": 32,
        "rating": 4.5
    },
    {
        "name": "Water-Resistant Canvas Laptop Backpack",
        "description": "Spacious commuter backpack with padded 15.6-inch laptop sleeve, external USB charging port, and luggage strap.",
        "category": "Accessories",
        "price": 46.99,
        "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80",
        "stock": 25,
        "rating": 4.9
    }
]

DEMO_USERS = [
    {
        "name": "Store Administrator",
        "email": "admin@ecommerce.com",
        "password": "adminpassword123",
        "role": "admin"
    },
    {
        "name": "Demo Student",
        "email": "student@ecommerce.com",
        "password": "studentpassword123",
        "role": "user"
    }
]


def seed_database(force_refresh=False):
    """
    Seeds initial products and demo users if they don't already exist.
    If force_refresh is True, clears existing products and re-inserts them.
    """
    products_coll = get_products_collection()
    users_coll = get_users_collection()

    print("[Seed] Checking database collections...")

    # Seed Users
    for user_info in DEMO_USERS:
        existing = users_coll.find_one({"email": user_info["email"]})
        if not existing:
            hashed = generate_password_hash(user_info["password"], method="scrypt")
            doc = {
                "name": user_info["name"],
                "email": user_info["email"],
                "password": hashed,
                "role": user_info["role"],
                "created_at": datetime.now(timezone.utc)
            }
            users_coll.insert_one(doc)
            print(f"[Seed] Created demo user: {user_info['email']} ({user_info['role']})")
        else:
            print(f"[Seed] Demo user already exists: {user_info['email']}")

    # Seed Products
    existing_count = products_coll.count_documents({})
    if existing_count == 0 or force_refresh:
        if force_refresh and existing_count > 0:
            products_coll.delete_many({})
            print("[Seed] Cleared existing products for refresh.")

        now = datetime.now(timezone.utc)
        inserted_count = 0
        for prod in SAMPLE_PRODUCTS:
            doc = dict(prod)
            doc["created_at"] = now
            res = products_coll.insert_one(doc)
            # Add string product_id matching _id
            products_coll.update_one({"_id": res.inserted_id}, {"$set": {"product_id": str(res.inserted_id)}})
            inserted_count += 1

        print(f"[Seed] Successfully seeded {inserted_count} sample products across 5 categories.")
    else:
        print(f"[Seed] Products collection already has {existing_count} products. Skipping product seeding.")

    return True


if __name__ == "__main__":
    print("Connecting to MongoDB to seed sample data...")
    is_connected, msg = test_connection()
    if is_connected:
        print(msg)
        seed_database()
        print("Database seeding completed successfully!")
    else:
        print(f"Connection test failed:\n{msg}")
