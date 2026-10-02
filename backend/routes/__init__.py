"""
Routes package for the Flask e-commerce backend.
Exports all blueprints for registration in app.py.
"""

from .auth import auth_bp
from .products import products_bp
from .cart import cart_bp
from .orders import orders_bp
from .admin import admin_bp

__all__ = ["auth_bp", "products_bp", "cart_bp", "orders_bp", "admin_bp"]
