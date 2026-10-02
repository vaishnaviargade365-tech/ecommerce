# Development Plan

This document defines the implementation order. It contains planning only and does not contain source code.

## Phase 1 — Project Setup

Create:

```text
/client
/server
```

Prepare the specified MERN stack and Tailwind CSS environment.

## Phase 2 — Database Models

Create only:

```text
User
Category
Product
Order
```

Define the required fields and relationships.

## Phase 3 — Authentication

Implement:
- Customer registration
- Customer login
- Logout
- Admin login
- JWT authentication
- bcrypt password hashing
- Auth middleware
- Admin middleware

## Phase 4 — Category Management

Implement admin operations:
- View
- Add
- Edit
- Delete

## Phase 5 — Product Management

Implement admin operations:
- View
- Add
- Edit
- Delete

Include:
- Category
- Price
- Stock
- Image
- Description

## Phase 6 — Public Product Website

Build:
- Home
- Products
- Product Details
- Search
- Category filter
- Responsive product grid

## Phase 7 — Cart

Implement:
- Add to cart
- Increase quantity
- Decrease quantity
- Remove product
- Total calculation
- Stock limit

## Phase 8 — Checkout and Orders

Implement:
- Checkout form
- Cash on Delivery
- Stock validation
- Database price validation
- Order creation
- Stock reduction
- Cart clearing

## Phase 9 — My Orders

Allow customers to view their own orders.

## Phase 10 — Admin Orders

Allow admin to:
- View all orders
- View order details
- Update order status

## Phase 11 — UI/UX

Add:
- Responsive design
- Toast messages
- Loading states
- Empty states
- Confirmation dialogs

## Phase 12 — Integration Testing

Verify the complete demo flow:

```text
Admin Login
→ Category
→ Product
→ Customer Registration/Login
→ Browse
→ Filter
→ Cart
→ Checkout
→ Order
→ Admin Order View
→ Status Update
```

## Out of Scope

Do not add:
- Payment gateway
- Wishlist
- Reviews
- Coupons
- Suppliers
- Multi-vendor features
- Advanced analytics
