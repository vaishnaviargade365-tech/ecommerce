# Mini E-Commerce Demo Project

## Overview

A small, clean and responsive **MERN Stack Mini E-Commerce Demo Project**.

The project has two parts:

```text
/client  → React frontend
/server  → Node.js + Express backend
```

## Tech Stack

- Frontend: React.js + Vite + JavaScript
- Styling: Tailwind CSS
- Backend: Node.js + Express.js
- Database: MongoDB + Mongoose
- Authentication: JWT + bcrypt
- API calls: Axios

## Main Features

### Customer
- Register
- Login
- Logout
- Browse products
- Search products
- Filter by category
- Add products to cart
- Increase/decrease quantity
- Remove products
- Checkout using Cash on Delivery
- View own orders

### Admin
- Admin login
- Protected admin routes
- Manage categories
- Manage products
- View customer orders
- View order details
- Update order status

## Order Status

```text
Pending
Confirmed
Shipped
Delivered
Cancelled
```

## Main Demo Flow

```text
Admin Login
   ↓
Add Category
   ↓
Add Product
   ↓
Product appears on Website
   ↓
User Register/Login
   ↓
Browse Products
   ↓
Filter by Category
   ↓
Add to Cart
   ↓
Checkout
   ↓
Place Order
   ↓
Order saved in MongoDB
   ↓
Admin sees Order
   ↓
Admin updates Order Status
```

## Scope

This is intentionally a mini project.

The project does not include:
- Payment gateway
- Wishlist
- Reviews
- Coupons
- Suppliers
- Multi-vendor features
- Advanced analytics
