# Mini E-Commerce Demo — 2-Person Work Distribution & Git Roadmap

This document outlines the complete distribution of responsibilities, file/folder ownership, Git branching strategy, and step-by-step merge process for two developers collaborating on the Mini E-Commerce project.

---

## 1. Team Roles & Folder Ownership Matrix

To completely eliminate merge conflicts, the project is divided by architectural boundary:

| Parameter | **Person 1 (Backend & Database)** | **Person 2 (Frontend & UI/UX)** |
| :--- | :--- | :--- |
| **Primary Domain** | Server, API, Database, Security | Client UI, State, Routing, Styling |
| **Exclusive Folder** | `/server/` | `/client/` |
| **Tech Stack** | Node.js, Express, MongoDB, Mongoose, JWT, bcrypt | React.js, Vite, Tailwind CSS, Axios, Lucide Icons |
| **Primary Git Branch** | `feature/backend-api` | `feature/frontend-ui` |
| **Testing Tool** | Postman / Thunder Client | Browser & DevTools |

---

## 2. File & Directory Breakdown

```text
mini-ecommerce/
├── .gitignore
├── README.md
├── (Documentation files...)
│
├── server/                                  <── [PERSON 1 EXCLUSIVE]
│   ├── config/
│   │   └── db.js                            # MongoDB connection logic
│   ├── controllers/
│   │   ├── authController.js                # Customer & Admin login/register
│   │   ├── categoryController.js            # Category CRUD handlers
│   │   ├── productController.js             # Product CRUD & search/filter handlers
│   │   └── orderController.js               # Order placement & status handlers
│   ├── middleware/
│   │   └── authMiddleware.js                # JWT verification & admin role check
│   ├── models/
│   │   ├── User.js                          # Customer & Admin schema
│   │   ├── Category.js                      # Category schema
│   │   ├── Product.js                       # Product schema
│   │   └── Order.js                         # Order schema
│   ├── routes/
│   │   ├── authRoutes.js                    # /api/auth
│   │   ├── categoryRoutes.js                # /api/categories
│   │   ├── productRoutes.js                 # /api/products
│   │   └── orderRoutes.js                   # /api/orders & /api/admin/orders
│   ├── .env.example                         # PORT, MONGO_URI, JWT_SECRET
│   ├── package.json                         # express, mongoose, bcryptjs, jsonwebtoken, cors, dotenv
│   └── server.js                            # Express app entry & middleware wiring
│
└── client/                                  <── [PERSON 2 EXCLUSIVE]
    ├── public/                              # Static logos and assets
    ├── src/
    │   ├── api/
    │   │   └── axios.js                     # Axios instance with baseURL & JWT interceptor
    │   ├── components/
    │   │   ├── Navbar.jsx                   # Navigation, cart badge, login/logout links
    │   │   ├── Footer.jsx                   # Simple footer
    │   │   ├── ProductCard.jsx              # Product card with Add-to-Cart
    │   │   ├── ProtectedRoute.jsx           # Customer & Admin route guard
    │   │   ├── Toast.jsx                    # Action feedback toasts
    │   │   └── Modal.jsx                    # Delete & confirmation dialogs
    │   ├── context/
    │   │   ├── AuthContext.jsx              # Login state, token, user profile, role
    │   │   └── CartContext.jsx              # Cart items, add/remove, qty limits, total
    │   ├── pages/
    │   │   ├── Home.jsx                     # Hero section & featured products
    │   │   ├── Products.jsx                 # Product listing, search & category filters
    │   │   ├── ProductDetails.jsx           # Single product view & stock check
    │   │   ├── Cart.jsx                     # Cart list, quantity modifiers, total
    │   │   ├── Checkout.jsx                 # Shipping address form & COD submit
    │   │   ├── MyOrders.jsx                 # Customer order history & status badge
    │   │   ├── Login.jsx                    # Customer & Admin sign-in
    │   │   ├── Register.jsx                 # New customer registration
    │   │   └── admin/
    │   │       ├── Dashboard.jsx            # Admin summary
    │   │       ├── ManageCategories.jsx     # Category list, add/edit/delete modal
    │   │       ├── ManageProducts.jsx       # Product table, add/edit/delete modal
    │   │       └── ManageOrders.jsx         # Orders table & status dropdown updater
    │   ├── App.jsx                          # Route definitions & Context providers
    │   ├── main.jsx                         # React root mount
    │   └── index.css                        # Tailwind CSS directives
    ├── index.html                           # App shell
    ├── tailwind.config.js                   # Tailwind theme & color setup
    ├── vite.config.js                       # Vite configuration
    └── package.json                         # react, react-router-dom, axios, lucide-react
```

---

## 3. Step-by-Step Task Distribution

### **Person 1: Backend & Database Roadmap (`/server`)**

* [ ] **Step 1 — Project Initialization**:
  - Initialize `server/package.json` and install: `express`, `mongoose`, `dotenv`, `cors`, `bcryptjs`, `jsonwebtoken`.
  - Create `server.js` with CORS and JSON body parser.
  - Setup `config/db.js` to connect to MongoDB.
  - Create `.env.example` with `PORT=5000`, `MONGO_URI`, and `JWT_SECRET`.
* [ ] **Step 2 — Data Models**:
  - `models/User.js`: fields `name`, `email` (unique), `password` (hashed), `role` (`customer` / `admin`).
  - `models/Category.js`: fields `name`, `description`.
  - `models/Product.js`: fields `name`, `description`, `price` (> 0), `image`, `category` (ref Category), `stock` (>= 0).
  - `models/Order.js`: fields `user` (ref User), `products` array, `totalAmount`, `shippingAddress`, `status` (enum: `Pending`, `Confirmed`, `Shipped`, `Delivered`, `Cancelled`), timestamps.
* [ ] **Step 3 — Security & Authentication**:
  - Implement `controllers/authController.js` for `POST /api/auth/register` and `POST /api/auth/login`.
  - Create `middleware/authMiddleware.js`:
    - `protect`: verifies Bearer JWT token and attaches `req.user`.
    - `admin`: validates that `req.user.role === 'admin'`.
* [ ] **Step 4 — Category Endpoints**:
  - `GET /api/categories`: Public list of all categories.
  - `POST /api/categories`: Admin only (Add category).
  - `PUT /api/categories/:id`: Admin only (Update category).
  - `DELETE /api/categories/:id`: Admin only (Delete category).
* [ ] **Step 5 — Product Endpoints**:
  - `GET /api/products`: Public query with category filter (`?category=id`) and search keyword (`?search=query`).
  - `GET /api/products/:id`: Public single product lookup.
  - `POST`, `PUT`, `DELETE /api/products/:id`: Admin only endpoints.
* [ ] **Step 6 — Order Processing Endpoints (Crucial Business Logic)**:
  - `POST /api/orders`: Authenticated customer order placement.
    - **Rule**: Fetch product prices directly from MongoDB to compute the total; never trust client-sent prices.
    - **Rule**: Validate available stock before confirming order; decrement stock upon creation.
  - `GET /api/orders/my-orders`: List orders for the logged-in customer.
  - `GET /api/admin/orders`: Admin list of all customer orders.
  - `PATCH /api/admin/orders/:id/status`: Admin status updater (`Pending` → `Confirmed` → `Shipped` → `Delivered` / `Cancelled`).
* [ ] **Step 7 — API Verification**:
  - Test every route using Postman or Thunder Client to ensure proper HTTP status codes and error responses.

---

### **Person 2: Frontend & UI/UX Roadmap (`/client`)**

* [ ] **Step 1 — Project Initialization**:
  - Scaffold React with Vite inside `/client`.
  - Install dependencies: `react-router-dom`, `axios`, `lucide-react`, `tailwindcss`, `postcss`, `autoprefixer`.
  - Initialize Tailwind CSS configuration and setup clean layout styles.
* [ ] **Step 2 — Axios Setup & Authentication State**:
  - Create `src/api/axios.js` configured with `baseURL: 'http://localhost:5000/api'`.
  - Add an Axios request interceptor that automatically attaches `Authorization: Bearer <token>` from `localStorage`.
  - Implement `AuthContext.jsx` (`user`, `token`, `login()`, `logout()`, `role`).
  - Build `components/ProtectedRoute.jsx` for both Customer and Admin route security.
* [ ] **Step 3 — Public Storefront & Product Browsing**:
  - Build `Navbar.jsx` with logo, navigation links, live cart badge counter, and auth status.
  - Build `Home.jsx` with clean banner and quick category tiles.
  - Build `Products.jsx` featuring:
    - Search input field.
    - Category filter pill buttons (`All`, `Electronics`, `Fashion`, etc.).
    - Responsive product cards displaying image, title, category, price, and stock badge.
  - Build `ProductDetails.jsx` with full description, stock availability check, and quantity selector.
* [ ] **Step 4 — Cart Management (`CartContext.jsx`)**:
  - State management for cart items stored in `localStorage`.
  - Actions: `addToCart(product, qty)`, `increaseQty(productId)`, `decreaseQty(productId)`, `removeFromCart(productId)`, `clearCart()`.
  - Boundary: Prevent quantity from exceeding product's available `stock`.
  - Build `Cart.jsx` showing order summary, subtotal calculation, and "Proceed to Checkout" button.
* [ ] **Step 5 — Checkout & Customer Orders**:
  - Build `Checkout.jsx` form: Name, Phone, Shipping Address, City, Pincode, and fixed "Cash on Delivery" radio selection.
  - On submit: Dispatch order payload to API, clear cart upon success, and redirect to orders page.
  - Build `MyOrders.jsx`: Table/cards displaying user's order date, ordered items, total amount, and color-coded status badges.
* [ ] **Step 6 — Admin Dashboard**:
  - Build admin navigation / sidebar.
  - Build `ManageCategories.jsx`: Table of categories with Add/Edit modal dialogs and Delete confirmation.
  - Build `ManageProducts.jsx`: Table of products with stock indicators, Add/Edit modal (name, price, stock, category dropdown, image URL), and Delete action.
  - Build `ManageOrders.jsx`: Table of all customer orders with order details expandable and status update dropdown.
* [ ] **Step 7 — UI Polish & Feedback**:
  - Add toast alerts for success/failure feedback (e.g. "Item added to cart", "Order placed").
  - Add loading spinners for async actions and empty-state placeholders (e.g. "Cart is empty", "No products found").

---

## 4. Git Collaboration & Branching Plan

Both developers will clone the repository and work on separate feature branches.

### **Initial Setup (Both Developers)**

Each person configures their Git credentials:

```bash
# Person 1 (Vaishnavi)
git config --global user.name "Vaishnavi Argade"
git config --global user.email "vaishnaviargade365@gmail.com"

# Person 2 (Partner)
git config --global user.name "Partner Name"
git config --global user.email "partner@example.com"
```

Clone the repository:
```bash
git clone https://github.com/vaishnaviargade365-tech/ecommerce.git
cd ecommerce
```

---

### **Person 1 Workflow (Backend)**

```bash
# 1. Switch to a new backend feature branch
git checkout -b feature/backend-api

# 2. Work inside the /server directory, commit in logical chunks
git add server/
git commit -m "feat(server): setup express server and mongodb connection"

git add server/
git commit -m "feat(auth): implement user model and JWT authentication"

git add server/
git commit -m "feat(api): add category, product and order endpoints"

# 3. Push branch to GitHub
git push -u origin feature/backend-api
```

---

### **Person 2 Workflow (Frontend)**

```bash
# 1. Switch to a new frontend feature branch
git checkout -b feature/frontend-ui

# 2. Work inside the /client directory, commit in logical chunks
git add client/
git commit -m "feat(client): setup vite react app with tailwind css"

git add client/
git commit -m "feat(ui): add navbar, storefront, search and category filters"

git add client/
git commit -m "feat(cart): implement cart context and checkout flow"

git add client/
git commit -m "feat(admin): build admin dashboard and order management"

# 3. Push branch to GitHub
git push -u origin feature/frontend-ui
```

---

## 5. How to Merge at the End (Step-by-Step Integration)

Because Person 1 only touches `/server` and Person 2 only touches `/client`, the merge will be **100% clean with zero file conflicts**.

Follow these exact steps when both sides finish their tasks:

### **Step 1: Merge Backend to `main`**

Person 1 merges `feature/backend-api` first:
```bash
git checkout main
git pull origin main
git merge feature/backend-api
git push origin main
```
*(Or open a Pull Request on GitHub from `feature/backend-api` into `main` and click "Merge pull request".)*

---

### **Step 2: Rebase / Sync Frontend with `main`**

Person 2 updates their local repository with the backend code:
```bash
git checkout main
git pull origin main

git checkout feature/frontend-ui
git merge main
```
*Since `/server` and `/client` are completely separate directories, Git will perform a fast, automatic merge.*

---

### **Step 3: Merge Frontend to `main`**

Person 2 merges `feature/frontend-ui` into `main`:
```bash
git checkout main
git merge feature/frontend-ui
git push origin main
```
*(Or open a Pull Request on GitHub from `feature/frontend-ui` into `main` and click "Merge".)*

---

### **Step 4: End-to-End Verification (Both Developers Together)**

Now that `main` has both `/server` and `/client`:

1. **Terminal 1 (Backend)**:
   ```bash
   cd server
   npm install
   # Ensure .env has valid MONGO_URI and JWT_SECRET
   npm run dev    # or node server.js
   ```
2. **Terminal 2 (Frontend)**:
   ```bash
   cd client
   npm install
   npm run dev
   ```
3. **Execute the Complete [DEMO_FLOW.md](DEMO_FLOW.md)**:
   - [ ] Log in as Admin.
   - [ ] Create Categories (`Electronics`, `Fashion`, `Footwear`).
   - [ ] Add Products with price, stock, and image URLs.
   - [ ] Log out of Admin.
   - [ ] Register a new Customer account and sign in.
   - [ ] Browse products, search by keyword, and filter by category.
   - [ ] Add items to cart; verify stock limit warnings.
   - [ ] Proceed to Checkout, enter delivery details, select Cash on Delivery, and place order.
   - [ ] Check "My Orders" as customer; verify order status says `Pending`.
   - [ ] Log back in as Admin, view orders list, and update status to `Confirmed` → `Shipped` → `Delivered`.
