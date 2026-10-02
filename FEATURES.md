# Features

## 1. Authentication

### Customer Authentication
- Register
- Login
- Logout

Registration fields:
- Name
- Email
- Password
- Confirm Password

### Admin Authentication
- Admin Login
- JWT protected admin routes

Security requirements:
- Password hashing with bcrypt
- JWT token authentication
- Authentication middleware
- Admin middleware

## 2. Categories

Admin operations:
- Add category
- Edit category
- Delete category
- View categories

Fields:
- Name
- Description

## 3. Products

Admin operations:
- Add product
- Edit product
- Delete product
- View products

Fields:
- Product name
- Description
- Price
- Image
- Category
- Stock

## 4. Public Website

Pages:

```text
Home
Products
Product Details
Cart
Checkout
Login
Register
My Orders
```

Product features:
- Product image
- Product name
- Price
- Category
- Add to Cart
- Category filter
- Product search
- Responsive product grid

Example category filter:

```text
All | Electronics | Fashion | Shoes
```

## 5. Cart

Customers can:
- Add product
- Increase quantity
- Decrease quantity
- Remove product
- View total price

Quantity must not exceed available stock.

## 6. Checkout

Checkout fields:
- Name
- Phone
- Address
- City
- Pincode

Payment method:

```text
Cash on Delivery
```

## 7. Orders

Customer:
- Place order
- View own orders

Admin:
- View all orders
- View order details
- Change order status

## 8. UI/UX

The interface should be:
- Modern
- Clean
- User-friendly
- Responsive
- Mobile compatible
- Tablet compatible
- Desktop compatible

UI elements:
- Cards
- Responsive navbar
- Admin sidebar
- Admin tables
- Toast messages
- Loading states
- Empty states
- Delete confirmation dialog
