# API Documentation

Base API prefix:

```text
/api
```

## Authentication

### Register

```text
POST /api/auth/register
```

Purpose:
Create a customer account.

### Login

```text
POST /api/auth/login
```

Purpose:
Authenticate a customer or appropriate authentication flow.

## Categories

### Get Categories

```text
GET /api/categories
```

### Add Category

```text
POST /api/categories
```

Admin protected.

### Edit Category

```text
PUT /api/categories/:id
```

Admin protected.

### Delete Category

```text
DELETE /api/categories/:id
```

Admin protected.

## Products

### Get Products

```text
GET /api/products
```

Supports filtering and searching:

```text
GET /api/products?category=electronics&search=phone
```

### Get Product Details

```text
GET /api/products/:id
```

### Add Product

```text
POST /api/products
```

Admin protected.

### Edit Product

```text
PUT /api/products/:id
```

Admin protected.

### Delete Product

```text
DELETE /api/products/:id
```

Admin protected.

## Orders

### Create Order

```text
POST /api/orders
```

Customer authentication required.

Order creation must:
1. Validate stock.
2. Fetch current product prices from MongoDB.
3. Calculate the order total using database prices.
4. Create the order.
5. Reduce product stock.
6. Clear the cart.

### My Orders

```text
GET /api/orders/my-orders
```

Customer authentication required.

### Admin Orders

```text
GET /api/admin/orders
```

Admin authentication required.

### Update Order Status

```text
PATCH /api/admin/orders/:id/status
```

Admin authentication required.

Allowed statuses:

```text
Pending
Confirmed
Shipped
Delivered
Cancelled
```
