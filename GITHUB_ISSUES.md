# GitHub Issues & Task Breakdown (2-Person Team)

Copy and paste these issue templates directly into your GitHub repository's **Issues** tab to track the project development.

---

## 📋 Overview of Issues & Assignment

| Issue # | Title | Assignee | Primary Branch | Category |
| :---: | :--- | :--- | :--- | :--- |
| **#1** | [Backend] Database Schemas & Models Setup | **Person 1** | `feature/backend-api` | `backend`, `database` |
| **#2** | [Backend] Authentication & Authorization Middleware | **Person 1** | `feature/backend-api` | `backend`, `security` |
| **#3** | [Backend] Category & Product Management APIs | **Person 1** | `feature/backend-api` | `backend`, `api` |
| **#4** | [Backend] Order Placement Engine & Admin Lifecycle | **Person 1** | `feature/backend-api` | `backend`, `business-logic` |
| **#5** | [Frontend] Vite Setup, Tailwind CSS & Auth/Cart Context | **Person 2** | `feature/frontend-ui` | `frontend`, `state` |
| **#6** | [Frontend] Storefront, Product Catalog & Search UI | **Person 2** | `feature/frontend-ui` | `frontend`, `ui` |
| **#7** | [Frontend] Cart Management, Checkout & Customer Orders | **Person 2** | `feature/frontend-ui` | `frontend`, `cart` |
| **#8** | [Frontend] Admin Dashboard & Management Portal | **Person 2** | `feature/frontend-ui` | `frontend`, `admin` |
| **#9** | [Integration] End-to-End Verification & Main Branch Merge | **Both** | `main` | `integration`, `testing` |

---

## 🛠️ Person 1: Backend Issues

### Issue #1: [Backend] Database Schemas & Models Setup
- **Assignee**: Person 1 (Backend Developer)
- **Labels**: `backend`, `database`
- **Branch**: `feature/backend-api`

#### Description
Implement the 4 required Mongoose data models in `server/models/` strictly according to `DATABASE_SCHEMA.md`.

#### Files to Touch
- `server/models/User.js`
- `server/models/Category.js`
- `server/models/Product.js`
- `server/models/Order.js`

#### Tasks & Acceptance Criteria
- [ ] **User Model**:
  - Fields: `name` (String, required), `email` (String, required, unique), `password` (String, required), `role` (String, enum: `['customer', 'admin']`, default: `'customer'`).
- [ ] **Category Model**:
  - Fields: `name` (String, required, unique), `description` (String).
- [ ] **Product Model**:
  - Fields: `name` (String, required), `description` (String), `price` (Number, required, min: 0), `image` (String, required), `category` (ObjectId referencing Category), `stock` (Number, required, min: 0).
- [ ] **Order Model**:
  - Fields: `user` (ObjectId referencing User), `products` array with `product` (ObjectId ref Product), `quantity` (Number), `price` (Number), `totalAmount` (Number), `shippingAddress` (Object with address, city, pincode, phone), `status` (enum: `['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled']`, default: `'Pending'`), timestamps.

---

### Issue #2: [Backend] Authentication & Authorization Middleware
- **Assignee**: Person 1 (Backend Developer)
- **Labels**: `backend`, `security`, `auth`
- **Branch**: `feature/backend-api`

#### Description
Implement customer/admin registration and login with bcrypt password hashing, JWT generation, and route protection middlewares according to `AUTHENTICATION.md`.

#### Files to Touch
- `server/controllers/authController.js`
- `server/middleware/authMiddleware.js`
- `server/routes/authRoutes.js`
- `server/server.js` (wire route)

#### Tasks & Acceptance Criteria
- [ ] **`POST /api/auth/register`**: Validate required fields, check unique email, hash password with `bcryptjs`, save user, return JWT + user info (id, name, email, role).
- [ ] **`POST /api/auth/login`**: Validate credentials against database hash, return JWT + user info.
- [ ] **`authMiddleware.js`**:
  - `protect`: Extracts Bearer token from headers, verifies with `JWT_SECRET`, attaches `req.user` (excluding password).
  - `admin`: Checks if `req.user.role === 'admin'`; returns 403 Forbidden if not.

---

### Issue #3: [Backend] Category & Product Management APIs
- **Assignee**: Person 1 (Backend Developer)
- **Labels**: `backend`, `api`
- **Branch**: `feature/backend-api`

#### Description
Implement public browsing endpoints and admin-protected CRUD operations for categories and products according to `API_DOCUMENTATION.md`.

#### Files to Touch
- `server/controllers/categoryController.js`
- `server/routes/categoryRoutes.js`
- `server/controllers/productController.js`
- `server/routes/productRoutes.js`

#### Tasks & Acceptance Criteria
- [ ] **Categories**:
  - `GET /api/categories` (Public): Return all categories.
  - `POST /api/categories` (Admin only): Create new category.
  - `PUT /api/categories/:id` (Admin only): Update category name/description.
  - `DELETE /api/categories/:id` (Admin only): Remove category.
- [ ] **Products**:
  - `GET /api/products` (Public): Support filtering by `?category=<categoryId>` and searching by `?search=<keyword>`.
  - `GET /api/products/:id` (Public): Return product details populated with category.
  - `POST /api/products` (Admin only): Validate price > 0, stock >= 0, and save product.
  - `PUT /api/products/:id` (Admin only): Edit product details.
  - `DELETE /api/products/:id` (Admin only): Remove product.

---

### Issue #4: [Backend] Order Placement Engine & Admin Lifecycle
- **Assignee**: Person 1 (Backend Developer)
- **Labels**: `backend`, `business-logic`, `orders`
- **Branch**: `feature/backend-api`

#### Description
Implement order placement with critical business rules (server-side price verification and stock decrement) and status update endpoints according to `API_DOCUMENTATION.md`.

#### Files to Touch
- `server/controllers/orderController.js`
- `server/routes/orderRoutes.js`

#### Tasks & Acceptance Criteria
- [ ] **`POST /api/orders`** (Customer protected):
  - **Security Rule**: Do NOT trust frontend prices. Query MongoDB for actual product prices.
  - Validate stock availability for each item.
  - Decrement product stock in MongoDB upon successful placement.
  - Save order with `Pending` status and `Cash on Delivery` payment method.
- [ ] **`GET /api/orders/my-orders`** (Customer protected): Return orders belonging to logged-in user sorted by newest.
- [ ] **`GET /api/admin/orders`** (Admin protected): Return all customer orders.
- [ ] **`PATCH /api/admin/orders/:id/status`** (Admin protected): Update order status (`Pending`, `Confirmed`, `Shipped`, `Delivered`, `Cancelled`).

---

## 🎨 Person 2: Frontend Issues

### Issue #5: [Frontend] Vite Setup, Tailwind CSS & Auth/Cart Context
- **Assignee**: Person 2 (Frontend Developer)
- **Labels**: `frontend`, `setup`, `state`
- **Branch**: `feature/frontend-ui`

#### Description
Scaffold the React application with Vite and Tailwind CSS inside `/client`, and establish global state management and API client according to `DEVELOPMENT_PLAN.md`.

#### Files to Touch
- `client/package.json`
- `client/tailwind.config.js`
- `client/src/api/axios.js`
- `client/src/context/AuthContext.jsx`
- `client/src/context/CartContext.jsx`
- `client/src/components/ProtectedRoute.jsx`

#### Tasks & Acceptance Criteria
- [ ] Scaffold React app with Vite inside `client/` and configure Tailwind CSS.
- [ ] Setup Axios instance with `baseURL: http://localhost:5000/api` and request interceptor attaching Bearer token from `localStorage`.
- [ ] Build `AuthContext`: Store user profile, token, `login()`, `logout()`, and role detection.
- [ ] Build `CartContext`: Manage `cartItems` in `localStorage`, `addToCart()`, `removeFromCart()`, `updateQty()`, and calculate subtotal.
- [ ] Create `ProtectedRoute` to restrict customer routes and admin routes.

---

### Issue #6: [Frontend] Storefront, Product Catalog & Search UI
- **Assignee**: Person 2 (Frontend Developer)
- **Labels**: `frontend`, `ui`, `storefront`
- **Branch**: `feature/frontend-ui`

#### Description
Build the public customer browsing experience with responsive layouts, search, category filter, and product cards according to `UI_UX.md`.

#### Files to Touch
- `client/src/components/Navbar.jsx`
- `client/src/components/ProductCard.jsx`
- `client/src/pages/Home.jsx`
- `client/src/pages/Products.jsx`
- `client/src/pages/ProductDetails.jsx`

#### Tasks & Acceptance Criteria
- [ ] `Navbar`: Responsive navigation, logo, links, real-time cart item count badge, user profile/logout button.
- [ ] `Home`: Hero banner and featured category buttons.
- [ ] `Products`:
  - Search input with debounce or instant query.
  - Category pill tabs (`All`, `Electronics`, `Fashion`, etc.).
  - Responsive product card grid showing image, name, price, stock badge, and "Add to Cart" button.
- [ ] `ProductDetails`: Display detailed image, description, price, in-stock badge, and quantity selector.

---

### Issue #7: [Frontend] Cart Management, Checkout & Customer Orders
- **Assignee**: Person 2 (Frontend Developer)
- **Labels**: `frontend`, `cart`, `checkout`
- **Branch**: `feature/frontend-ui`

#### Description
Build the customer purchase journey: Cart view, Cash on Delivery checkout form, and order history page.

#### Files to Touch
- `client/src/pages/Cart.jsx`
- `client/src/pages/Checkout.jsx`
- `client/src/pages/MyOrders.jsx`

#### Tasks & Acceptance Criteria
- [ ] `Cart`: List items, increment/decrement quantity (disallow exceeding stock limit), remove item, show order summary, and empty state.
- [ ] `Checkout`: Form with Name, Phone, Address, City, Pincode, fixed "Cash on Delivery" option, and "Place Order" button.
- [ ] Clear cart state after successful order submission.
- [ ] `MyOrders`: Display user's placed orders, order ID, items list, total, and color-coded status badge (`Pending`, `Confirmed`, `Shipped`, `Delivered`).

---

### Issue #8: [Frontend] Admin Dashboard & Management Portal
- **Assignee**: Person 2 (Frontend Developer)
- **Labels**: `frontend`, `admin`, `ui`
- **Branch**: `feature/frontend-ui`

#### Description
Build the admin management interface with dedicated views for category management, product inventory, and customer order statuses.

#### Files to Touch
- `client/src/pages/admin/Dashboard.jsx`
- `client/src/pages/admin/ManageCategories.jsx`
- `client/src/pages/admin/ManageProducts.jsx`
- `client/src/pages/admin/ManageOrders.jsx`
- `client/src/components/Modal.jsx`

#### Tasks & Acceptance Criteria
- [ ] `Dashboard`: Admin navigation sidebar and summary statistics.
- [ ] `ManageCategories`: Table of categories with Add/Edit modal dialogs and Delete confirmation.
- [ ] `ManageProducts`: Table of products showing stock and price, with Add/Edit modal (including image URL and category dropdown) and Delete confirmation.
- [ ] `ManageOrders`: Table displaying all customer orders with customer info, address, items, and status updater dropdown (`Pending` → `Delivered`).

---

## 🚀 Both: Integration & Verification

### Issue #9: [Integration] End-to-End Verification & Main Branch Merge
- **Assignee**: Person 1 & Person 2 (Joint effort)
- **Labels**: `integration`, `testing`
- **Branch**: `main`

#### Tasks & Acceptance Criteria
- [ ] Person 1 merges `feature/backend-api` into `main`.
- [ ] Person 2 syncs `main` into `feature/frontend-ui`, then merges `feature/frontend-ui` into `main`.
- [ ] Test complete workflow per `DEMO_FLOW.md`:
  1. Admin logs in → creates Category → adds Product with stock.
  2. Customer registers → browses catalog → filters by Category → adds to Cart.
  3. Customer checks out with Cash on Delivery → order is created in MongoDB.
  4. Customer views order under "My Orders" with `Pending` status.
  5. Admin views order list and updates status to `Confirmed` → `Shipped` → `Delivered`.
