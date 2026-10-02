# Project Overview

## Project Name

Mini E-Commerce Demo Project

## Architecture

```text
React + Vite + Tailwind CSS
          |
        Axios
          |
     Express REST API
          |
      Mongoose
          |
       MongoDB
```

## Project Structure

```text
/client
/server
```

## User Roles

### Customer

Customers can:
- Register and login
- Browse products
- Search and filter products
- Manage their cart
- Place Cash on Delivery orders
- View their orders

### Admin

Admin can:
- Login through the admin authentication flow
- Manage categories
- Manage products
- View all customer orders
- View order details
- Change order status

## Core Data Flow

```text
Customer
   ↓
React Website
   ↓
Axios API Request
   ↓
Express Backend
   ↓
MongoDB
```

## Admin Data Flow

```text
Admin
   ↓
Admin Dashboard
   ↓
Protected API
   ↓
Auth Middleware
   ↓
Admin Middleware
   ↓
MongoDB
```
