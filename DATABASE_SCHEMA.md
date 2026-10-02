# Database Schema

The project uses MongoDB with Mongoose.

Only these four models are required:

```text
User
Category
Product
Order
```

## User

Purpose: Store customer and admin authentication information.

Required information:

```text
Name
Email
Password
Role
```

Password must be stored as a bcrypt hash.

Email must be unique.

## Category

Fields:

```text
Name
Description
```

## Product

Fields:

```text
Product name
Description
Price
Image
Category
Stock
```

Rules:
- Price must be positive.
- Stock cannot be negative.
- Category must reference a valid category.

## Order

Required fields:

```text
user
products
totalAmount
shippingAddress
status
createdAt
```

Order products should contain the product information needed for the order.

## Relationships

```text
User
  |
  └── Order

Category
  |
  └── Product

Product
  |
  └── Order Product
```

## Important Order Rule

The frontend must never be trusted for product prices.

When an order is created:

```text
Frontend Cart
      ↓
Backend receives product IDs and quantities
      ↓
Backend fetches current prices from MongoDB
      ↓
Backend validates stock
      ↓
Backend calculates total
      ↓
Order is saved
```
