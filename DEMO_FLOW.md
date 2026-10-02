# Demo Flow

## Complete Demo

### Step 1: Admin Login

Admin logs in through the admin authentication flow.

### Step 2: Add Category

Admin creates a category, for example:

```text
Electronics
```

### Step 3: Add Product

Admin adds a product with:
- Product name
- Description
- Price
- Image
- Category
- Stock

### Step 4: Product Appears on Website

The product becomes available on the public Products page.

### Step 5: Customer Registration

A customer registers with:

```text
Name
Email
Password
Confirm Password
```

### Step 6: Customer Login

Customer logs in.

### Step 7: Browse Products

Customer:
- Views products
- Searches products
- Filters by category

### Step 8: Add to Cart

Customer adds a product and changes quantity.

Quantity cannot exceed available stock.

### Step 9: Checkout

Customer enters:

```text
Name
Phone
Address
City
Pincode
```

Payment method:

```text
Cash on Delivery
```

### Step 10: Place Order

The backend performs:

```text
Cart
 ↓
Validate stock
 ↓
Fetch current product prices
 ↓
Create Order
 ↓
Save Order in MongoDB
 ↓
Reduce Product Stock
 ↓
Clear Cart
```

### Step 11: My Orders

Customer views the order in the My Orders page.

### Step 12: Admin Orders

Admin opens the Admin Panel and views the same customer order.

### Step 13: Update Status

Admin changes the order status:

```text
Pending
→ Confirmed
→ Shipped
→ Delivered
```

The order can also be marked:

```text
Cancelled
```
