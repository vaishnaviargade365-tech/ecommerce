# Team Work Distribution Plan (2 Persons)

This document provides two effective strategies to divide the **Mini E-Commerce Demo Project** between two developers, along with an integration roadmap and Git collaboration workflow.

---

## Strategy A: Frontend vs. Backend (Recommended)

This is the cleanest division of labor. It minimizes merge conflicts because each developer works in their own directory (`/client` vs `/server`).

### **Person 1: Backend & Database Engineer (`/server`)**

**Core Focus:** Data models, business logic, security, and RESTful APIs.

| Module | Tasks & Responsibilities | Key Files / Deliverables |
| :--- | :--- | :--- |
| **Environment & DB Setup** | Setup Express, connect MongoDB via Mongoose, configure `.env` | `server.js`, `config/db.js` |
| **Data Models** | Create Mongoose schemas for `User`, `Category`, `Product`, `Order` | `models/*.js` |
| **Authentication & Security** | Register & Login APIs, bcrypt password hashing, JWT generation | `controllers/authController.js`, `routes/authRoutes.js` |
| **Middlewares** | `authMiddleware` (verify token) & `adminMiddleware` (check role) | `middleware/auth.js` |
| **Category API** | CRUD endpoints (Get all, Add, Edit, Delete) with admin guards | `controllers/categoryController.js`, `routes/categoryRoutes.js` |
| **Product API** | CRUD endpoints with category filter, search query, stock validation | `controllers/productController.js`, `routes/productRoutes.js` |
| **Order Processing API** | Create order (validates stock, calculates total from DB price), `my-orders`, admin order list & status update | `controllers/orderController.js`, `routes/orderRoutes.js` |
| **Documentation & Testing** | Export Postman/Thunder Client collection, test API endpoints with mock requests | `postman_collection.json` |

---

### **Person 2: Frontend & UI/UX Engineer (`/client`)**

**Core Focus:** User interface, responsive design, client state management, and API integration.

| Module | Tasks & Responsibilities | Key Files / Deliverables |
| :--- | :--- | :--- |
| **Environment & Routing** | Setup Vite + React + Tailwind CSS, setup React Router | `App.jsx`, `main.jsx`, `tailwind.config.js` |
| **API Client & Auth State** | Axios instance with base URL & JWT interceptor, Auth Context / localStorage token handler | `src/api/axios.js`, `src/context/AuthContext.jsx` |
| **Public Storefront** | Navbar, Home banner, Product Grid, Search bar, Category filter tabs, Product Card | `src/pages/Home.jsx`, `src/pages/Products.jsx`, `src/components/ProductCard.jsx` |
| **Product Details & Cart** | Product detail view, Cart drawer/page with quantity increment/decrement, remove, total calculation | `src/pages/ProductDetails.jsx`, `src/context/CartContext.jsx`, `src/pages/Cart.jsx` |
| **Customer Checkout & Orders**| Checkout form (address, phone, COD selection), Order confirmation, "My Orders" history page | `src/pages/Checkout.jsx`, `src/pages/MyOrders.jsx` |
| **Admin Dashboard UI** | Admin layout/sidebar, Category management table + modal, Product management table + modal, Order status dropdown | `src/pages/admin/Dashboard.jsx`, `src/pages/admin/ManageProducts.jsx`, `src/pages/admin/ManageOrders.jsx` |
| **UI Polish & Feedback** | Toast notifications, loading spinners, empty states, confirmation dialogs, mobile responsiveness | `src/components/Navbar.jsx`, `src/components/Toast.jsx`, `src/components/Modal.jsx` |

---

## Strategy B: Feature-Based Split (Vertical Slices)

Both developers touch both frontend and backend, each owning a complete functional domain.

### **Person 1: Customer Storefront & Checkout Flow**
- **Backend:**
  - Customer Register & Login endpoints
  - Public Product & Category listing endpoints (search & filter)
  - Order placement endpoint (stock deduction & COD logic)
  - Customer "My Orders" endpoint
- **Frontend:**
  - Customer Auth pages (Login / Register)
  - Storefront, Search, Category filter, Product Cards, Product Details
  - Cart state management & Cart page
  - Checkout form and My Orders view

### **Person 2: Admin Dashboard & Inventory / Order Management**
- **Backend:**
  - Database Schemas (`User`, `Category`, `Product`, `Order`)
  - Admin authentication & `adminMiddleware`
  - Category CRUD APIs (Admin protected)
  - Product CRUD APIs (Admin protected)
  - Admin Order status update endpoints
- **Frontend:**
  - Admin login page & protected route wrapper
  - Admin Sidebar & Dashboard layout
  - Category management (table, add/edit modal, delete prompt)
  - Product management (table, image preview, add/edit modal, delete prompt)
  - Admin Order list & status changer dropdown

---

## Step-by-Step Collaboration Workflow

To ensure smooth teamwork and avoid Git conflicts:

```text
Day 1: Common Agreement & Initial Setup
├── Agree on API contracts (refer to API_DOCUMENTATION.md)
├── Agree on DB models (refer to DATABASE_SCHEMA.md)
└── Person 1 pushes initial boilerplate; Person 2 pulls

Days 2-4: Parallel Independent Development
├── Person 1 works on backend branch (or customer features)
└── Person 2 works on frontend branch (using mock data / Postman)

Day 5: Integration & End-to-End Testing
├── Connect React frontend with Express backend
├── Test complete demo flow (Admin adds product → Customer buys → Status updated)
└── Fix edge cases & polish UI
```

### Git Branching Best Practices

1. **Keep `main` protected / stable**: Only merge working features into `main`.
2. **Feature branches**:
   - `git checkout -b feature/server-auth`
   - `git checkout -b feature/client-storefront`
3. **Daily Sync**: Always run `git pull origin main` before starting new work.
