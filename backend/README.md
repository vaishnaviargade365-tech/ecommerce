# 🛒 Mini E-Commerce Flask Backend

A clean, beginner-friendly, and robust RESTful API backend for a student e-commerce website, built with **Python**, **Flask**, and **MongoDB Atlas** (using **PyMongo**).

---

## 📋 Table of Contents

1. [Backend Purpose](#1-backend-purpose)
2. [Technologies Used](#2-technologies-used)
3. [Project Structure](#3-project-structure)
4. [Step-by-Step Setup Guide](#4-step-by-step-setup-guide)
   - [4.1 Installing Python](#41-how-to-install-python)
   - [4.2 Creating a Virtual Environment](#42-how-to-create-a-virtual-environment)
   - [4.3 Installing Requirements](#43-how-to-install-requirements)
5. [MongoDB Atlas Setup Guide](#5-mongodb-atlas-setup-guide)
   - [5.1 Create an Atlas Project](#51-create-an-atlas-project)
   - [5.2 Create a Cluster / Deployment](#52-create-a-cluster--deployment)
   - [5.3 Create a Database User](#53-create-a-database-user)
   - [5.4 Network Access & IP Whitelisting](#54-network-access--ip-whitelisting)
   - [5.5 Obtain the Connection String](#55-obtain-the-connection-string)
6. [Configuring Environment Variables (.env)](#6-how-to-create-the-env-file)
7. [Starting the Flask Server](#7-how-to-start-the-flask-server)
8. [Seeding Demo Data](#8-seeding-demo-data)
9. [Automated Testing](#9-automated-testing)
10. [API Documentation](#10-api-documentation)
    - [Authentication Endpoints](#authentication-endpoints)
    - [Product Endpoints](#product-endpoints)
    - [Shopping Cart Endpoints](#shopping-cart-endpoints)
    - [Orders & Checkout Endpoints](#orders--checkout-endpoints)
    - [Admin Endpoints](#admin-endpoints)
11. [How the Frontend Connects to the Backend](#11-how-the-frontend-should-connect-to-the-backend)
12. [How Another Team Member Can Run Locally](#12-how-another-team-member-can-run-the-backend-locally)

---

## 1. Backend Purpose

This backend provides all data management and business logic for the student e-commerce platform:
- **Authentication**: Secure customer registration and login with encrypted passwords.
- **Product Catalog**: Browsing, single-product view, text search, and category filtering.
- **Shopping Cart**: Real-time cart synchronization, stock availability verification, and automatic total calculations.
- **Demo Checkout**: Instant order creation from cart, server-side price validation (prices from database are never trusted from the frontend), stock deduction, and order history tracking.
- **Admin Management**: Product management, inventory stock updates, order review, and order status updates (`Pending` → `Confirmed` → `Shipped` → `Delivered` / `Cancelled`).

---

## 2. Technologies Used

- **Python 3.10+**: Core programming language.
- **Flask**: Lightweight web framework for RESTful routing.
- **PyMongo (`pymongo[srv]`)**: Official MongoDB Python driver to connect with MongoDB Atlas.
- **Flask-CORS**: Enables Cross-Origin Resource Sharing so any frontend (React, Vite, Next.js, HTML) can make API calls.
- **python-dotenv**: Loads configuration and database secrets securely from `.env`.
- **Werkzeug**: Cryptographic password hashing (`generate_password_hash`, `check_password_hash`) using PBKDF2/scrypt.
- **mongomock**: In-memory MongoDB mock library used for offline and automated unit testing.

---

## 3. Project Structure

```text
backend/
│
├── app.py              # Main application entrypoint (Flask app, CORS, routes & errors)
├── config.py           # Configuration loader from .env
├── database.py         # PyMongo client, connection tester, indexes & collection accessors
├── requirements.txt    # Python dependencies
├── .env.example        # Template for required environment variables
├── .gitignore          # Ignores .env, virtual environments, and python cache
├── seed_data.py        # Realistic demo products across 5 categories + demo accounts
├── test_backend.py     # Comprehensive automated test suite (10 test modules)
├── README.md           # This documentation guide
│
├── routes/
│   ├── __init__.py     # Package initialization and blueprint exports
│   ├── auth.py         # Registration, Login, and User Profile
│   ├── products.py     # Product browsing, ID lookup, search, category filter
│   ├── cart.py         # Add, update quantity, remove, get, and clear cart
│   ├── orders.py       # Checkout, order creation, and order history
│   └── admin.py        # Admin product & stock management, order review & status
│
└── utils/
    ├── __init__.py     # Package initialization
    └── helpers.py      # Response formatters, ObjectId serialization, validation, admin check
```

---

## 4. Step-by-Step Setup Guide

### 4.1 How to Install Python

1. **Windows**:
   - Download the installer from [python.org](https://www.python.org/downloads/).
   - ⚠️ **Important**: During installation, check the box that says **"Add Python to PATH"**.
   - Verify in your terminal (PowerShell or Command Prompt):
     ```bash
     python --version
     ```
2. **macOS**:
   - Install via Homebrew: `brew install python` or download from [python.org](https://www.python.org/downloads/).
3. **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

---

### 4.2 How to Create a Virtual Environment

It is recommended to run the project in an isolated virtual environment:

```bash
# Navigate to the backend folder
cd backend

# Create a virtual environment named 'venv'
python -m venv venv
```

**Activate the virtual environment**:
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If PowerShell displays an Execution Policy error, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
- **Windows (Command Prompt / CMD)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

---

### 4.3 How to Install Requirements

With your virtual environment activated:

```bash
pip install -r requirements.txt
```

---

## 5. MongoDB Atlas Setup Guide

MongoDB Atlas provides a free cloud-hosted MongoDB database (`M0 Free Cluster`).

### 5.1 Create an Atlas Project
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) and sign in or create a free account.
2. In the top-left dropdown, click **"New Project"**.
3. Name it `Mini-Ecommerce` and click **"Create Project"**.

### 5.2 Create a Cluster / Deployment
1. Click **"Create Deployment"** (or **"Build a Database"**).
2. Choose the **M0 Free** tier (Free forever, 512 MB storage).
3. Select your closest AWS / Google Cloud region (e.g., `us-east-1` or `ap-south-1`).
4. Click **"Create Deployment"**.

### 5.3 Create a Database User
1. Under **"Quickstart"** or in the left sidebar under **"Database Access"**, click **"Add New Database User"**.
2. Authentication Method: **Password**.
3. Set a **Username** (e.g., `ecom_user`).
4. Set a secure **Password** (e.g., `StudentPass2026!`). Make sure to save this password!
5. User Privileges: Select **"Read and write to any database"**.
6. Click **"Add User"**.

### 5.4 Network Access & IP Whitelisting
1. In the left sidebar under **Security**, click **"Network Access"**.
2. Click **"Add IP Address"**.
3. Choose one of the following:
   - **For Local Development / Student Team (Recommended)**: Click **"Allow Access From Anywhere"** (`0.0.0.0/0`). This ensures you and your teammates can connect without worrying about changing home/campus Wi-Fi IPs.
   - **Or**: Click **"Add Current IP Address"**.
4. Click **"Confirm"**. It will take about 30 seconds to become active.

### 5.5 Obtain the Connection String
1. In the left sidebar under **Deployment**, click **"Database"**.
2. Click the **"Connect"** button next to your cluster.
3. Select **"Drivers"**.
4. Driver: **Python**, Version: **3.12 or later**.
5. Copy the connection string. It will look like:
   ```text
   mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<username>` and `<password>` with the database user you created in Step 5.3, and specify `/ecommerce_db` before the query parameter:
   ```text
   mongodb+srv://ecom_user:StudentPass2026!@cluster0.abcde.mongodb.net/ecommerce_db?retryWrites=true&w=majority
   ```

---

## 6. How to Create the `.env` File

Inside the `backend/` directory, create a file named `.env` by copying `.env.example`:

```bash
# Windows PowerShell
copy .env.example .env

# Mac / Linux
cp .env.example .env
```

Open `.env` and fill in your MongoDB Atlas connection string:

```env
# ==============================================================
# Environment Variables for Mini E-Commerce Backend
# ==============================================================
MONGO_URI=mongodb+srv://ecom_user:StudentPass2026!@cluster0.abcde.mongodb.net/ecommerce_db?retryWrites=true&w=majority
DB_NAME=ecommerce_db
PORT=5000
FLASK_ENV=development
SECRET_KEY=student-ecommerce-secret-key-2026
```

> ⚠️ **IMPORTANT**: Never commit your `.env` file to GitHub. The `.gitignore` file is already configured to keep `.env` private.

---

## 7. How to Start the Flask Server

Once `.env` is configured:

```bash
# Make sure you are inside the backend directory
cd backend

# Run the Flask app
python app.py
```

You will see:
```text
============================================================
  Starting Mini E-Commerce Flask Backend
  Port: 5000 | Environment: development
============================================================
[Database] Successfully connected to MongoDB Atlas!
[Database] Indexes created successfully.
 * Running on http://127.0.0.1:5000
```

---

## 8. Seeding Demo Data

The backend includes realistic demo products (Electronics, Clothing, Beauty, Home, Accessories) and demo user accounts.

To manually populate the database:
```bash
python seed_data.py
```

**Default Demo Accounts Created**:
- **Admin Account**:
  - Email: `admin@ecommerce.com`
  - Password: `adminpassword123`
  - Role: `admin`
- **Customer Account**:
  - Email: `student@ecommerce.com`
  - Password: `studentpassword123`
  - Role: `user`

---

## 9. Automated Testing

You can run the full test suite at any time (tests all 10 modules with mock or live database):

```bash
python test_backend.py
```

Expected output:
```text
======================================================================
  ALL TESTS PASSED SUCCESSFULLY! (10/10 MODULES VERIFIED)
======================================================================
```

---

## 10. API Documentation

Base URL:
```text
http://localhost:5000
```

All responses follow a consistent JSON format:
- **Success**:
  ```json
  {
    "success": true,
    "message": "Descriptive success message",
    "data": { ... }
  }
  ```
- **Error**:
  ```json
  {
    "success": false,
    "message": "Descriptive error message",
    "errors": [ ... ]
  }
  ```

---

### Authentication Endpoints

#### 1. Register User
- **Endpoint**: `POST /api/register` (or `POST /api/auth/register`)
- **Status Code**: `201 Created`
- **Request Body**:
  ```json
  {
    "name": "Alex Taylor",
    "email": "alex@university.edu",
    "password": "mypassword123",
    "role": "user"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "User registered successfully",
    "data": {
      "user_id": "674e2b10a...",
      "name": "Alex Taylor",
      "email": "alex@university.edu",
      "role": "user"
    }
  }
  ```

#### 2. User Login
- **Endpoint**: `POST /api/login` (or `POST /api/auth/login`)
- **Status Code**: `200 OK`
- **Request Body**:
  ```json
  {
    "email": "alex@university.edu",
    "password": "mypassword123"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Login successful",
    "data": {
      "user_id": "674e2b10a...",
      "name": "Alex Taylor",
      "email": "alex@university.edu",
      "role": "user"
    }
  }
  ```

#### 3. Get User Profile
- **Endpoint**: `GET /api/profile/<user_id>`
- **Status Code**: `200 OK`
- **Response**:
  ```json
  {
    "success": true,
    "message": "User profile retrieved successfully",
    "data": {
      "user_id": "674e2b10a...",
      "name": "Alex Taylor",
      "email": "alex@university.edu",
      "role": "user",
      "created_at": "2026-10-02T16:00:00"
    }
  }
  ```

---

### Product Endpoints

#### 1. Get All Products
- **Endpoint**: `GET /api/products`
- **Query Parameters (Optional)**:
  - `?category=Electronics` (filter by category)
  - `?search=headphones` (search by keyword)
  - `?sort=price_asc` / `price_desc` / `rating_desc`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Retrieved 17 products",
    "data": {
      "products": [
        {
          "product_id": "674e2b10a...",
          "name": "Wireless Noise-Cancelling Headphones",
          "description": "Premium over-ear wireless headphones...",
          "category": "Electronics",
          "price": 89.99,
          "image_url": "https://images.unsplash.com/...",
          "stock": 25,
          "rating": 4.8
        }
      ],
      "total": 17
    }
  }
  ```

#### 2. Get Single Product
- **Endpoint**: `GET /api/products/<product_id>`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Product details retrieved successfully",
    "data": {
      "product_id": "674e2b10a...",
      "name": "Wireless Noise-Cancelling Headphones",
      "description": "Premium over-ear wireless headphones...",
      "category": "Electronics",
      "price": 89.99,
      "image_url": "https://images.unsplash.com/...",
      "stock": 25,
      "rating": 4.8
    }
  }
  ```

#### 3. Search Products
- **Endpoint**: `GET /api/products/search?q=wireless`
- **Response**: Returns matching products by name, category, or description.

#### 4. Filter by Category
- **Endpoint**: `GET /api/products/category/<category>`
- **Example**: `GET /api/products/category/Clothing`

#### 5. Get Category List
- **Endpoint**: `GET /api/categories`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Categories retrieved successfully",
    "data": {
      "categories": [
        { "name": "Accessories", "count": 3 },
        { "name": "Beauty", "count": 3 },
        { "name": "Clothing", "count": 4 },
        { "name": "Electronics", "count": 4 },
        { "name": "Home", "count": 3 }
      ]
    }
  }
  ```

---

### Shopping Cart Endpoints

#### 1. Get Cart
- **Endpoint**: `GET /api/cart/<user_id>`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Cart retrieved successfully",
    "data": {
      "user_id": "674e2b10a...",
      "items": [
        {
          "product_id": "674e2b10a...",
          "name": "Wireless Noise-Cancelling Headphones",
          "price": 89.99,
          "quantity": 2,
          "subtotal": 179.98,
          "image_url": "https://...",
          "stock": 25
        }
      ],
      "total_price": 179.98,
      "total_items": 2
    }
  }
  ```

#### 2. Add Item to Cart
- **Endpoint**: `POST /api/cart`
- **Request Body**:
  ```json
  {
    "user_id": "674e2b10a...",
    "product_id": "674e2b10b...",
    "quantity": 1
  }
  ```
- *Note: Validates that requested quantity does not exceed available stock.*

#### 3. Update Cart Item Quantity
- **Endpoint**: `PUT /api/cart/<user_id>/<product_id>`
- **Request Body**:
  ```json
  {
    "quantity": 3
  }
  ```
- *Note: Setting quantity to 0 removes the item.*

#### 4. Remove Item from Cart
- **Endpoint**: `DELETE /api/cart/<user_id>/<product_id>`

#### 5. Clear Cart
- **Endpoint**: `DELETE /api/cart/<user_id>`

---

### Orders & Checkout Endpoints

#### 1. Place Order (Checkout)
- **Endpoint**: `POST /api/orders`
- **Status Code**: `201 Created`
- **Request Body**:
  ```json
  {
    "user_id": "674e2b10a...",
    "shipping_address": {
      "full_name": "Alex Taylor",
      "street": "123 Campus Lane, Dorm 5A",
      "city": "Boston",
      "state": "MA",
      "postal_code": "02115",
      "phone": "555-0123"
    },
    "payment_method": "Cash on Delivery (Demo Checkout)"
  }
  ```
- **Business Logic**:
  1. Checks stock availability.
  2. Calculates order total using current database prices.
  3. Deducts product stock in MongoDB.
  4. Automatically clears the user's cart.
  5. Returns created order.

#### 2. View User Order History
- **Endpoint**: `GET /api/orders/<user_id>`
- **Response**: List of user's past orders sorted by newest first.

#### 3. View Single Order Details
- **Endpoint**: `GET /api/orders/<user_id>/<order_id>`

---

### Admin Endpoints

> **Admin Protection**: Admin endpoints accept any of the following:
> - Header: `X-User-Role: admin`
> - Header: `X-User-Id: <admin_user_id>`
> - Query Parameter: `?role=admin`

#### 1. View All Products (Admin)
- **Endpoint**: `GET /api/admin/products`

#### 2. Add New Product
- **Endpoint**: `POST /api/admin/products`
- **Request Body**:
  ```json
  {
    "name": "Compact Mechanical Keyboard",
    "description": "RGB hot-swappable keyboard",
    "category": "Electronics",
    "price": 69.99,
    "image_url": "https://example.com/keyboard.jpg",
    "stock": 30,
    "rating": 4.7
  }
  ```

#### 3. Update Product Details
- **Endpoint**: `PUT /api/admin/products/<product_id>`
- **Request Body**: Any fields you wish to update (`price`, `stock`, `name`, etc.).

#### 4. Update Product Stock
- **Endpoint**: `PATCH /api/admin/products/<product_id>/stock`
- **Request Body**:
  ```json
  {
    "stock": 45
  }
  ```

#### 5. Delete Product
- **Endpoint**: `DELETE /api/admin/products/<product_id>`

#### 6. View All Customer Orders
- **Endpoint**: `GET /api/admin/orders`

#### 7. Update Order Status
- **Endpoint**: `PATCH /api/admin/orders/<order_id>/status`
- **Request Body**:
  ```json
  {
    "status": "Shipped"
  }
  ```
- *Allowed Statuses*: `Pending`, `Confirmed`, `Shipped`, `Delivered`, `Cancelled`

#### 8. Admin Dashboard Stats
- **Endpoint**: `GET /api/admin/stats`
- **Response**: Returns total products, total orders, total revenue, customer count, and low-stock count.

---

## 11. How the Frontend Should Connect to the Backend

### Base URL Configuration
In your frontend React/Vite project (e.g. `src/api.js` or `.env`):

```javascript
// src/api/client.js
const API_BASE_URL = "http://localhost:5000";

export default API_BASE_URL;
```

### Axios Example:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Example 1: Fetch Products
export const fetchProducts = async (category = '') => {
  const url = category ? `/products/category/${category}` : '/products';
  const response = await api.get(url);
  return response.data.data.products;
};

// Example 2: Add to Cart
export const addToCart = async (userId, productId, quantity = 1) => {
  const response = await api.post('/cart', {
    user_id: userId,
    product_id: productId,
    quantity: quantity
  });
  return response.data;
};

// Example 3: Checkout Order
export const placeOrder = async (userId, shippingAddress) => {
  const response = await api.post('/orders', {
    user_id: userId,
    shipping_address: shippingAddress
  });
  return response.data;
};
```

---

## 12. How Another Team Member Can Run the Backend Locally

Share these simple 4 steps with your teammate:

1. **Clone and checkout the `backend` branch**:
   ```bash
   git clone <repository_url>
   cd mini-ecommerce-docs
   git checkout backend
   cd backend
   ```
2. **Create virtual environment and install dependencies**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate

   pip install -r requirements.txt
   ```
3. **Set up `.env`**:
   Copy `.env.example` to `.env` and paste the shared team MongoDB Atlas connection string.
4. **Run the backend**:
   ```bash
   python app.py
   ```
   The backend server will automatically connect to MongoDB Atlas, create necessary indexes, and start listening on `http://localhost:5000`!
