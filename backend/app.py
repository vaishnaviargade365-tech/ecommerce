"""
Main Application Entrypoint for Mini E-Commerce Flask Backend.
Initializes:
- Flask application
- Flask-CORS for cross-origin requests from frontend (React, Vite, etc.)
- Blueprints for Auth, Products, Cart, Orders, Admin
- Centralized error handlers
- Health check and root status endpoints
"""

import sys
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database import test_connection, init_db
from routes import auth_bp, products_bp, cart_bp, orders_bp, admin_bp
from utils.helpers import error_response, success_response


def create_app(config_class=Config):
    """Application factory for Flask e-commerce backend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for all frontend clients
    # Allows requests from localhost:5173 (Vite), localhost:3000 (React/Next), or any origin
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        allow_headers=["Content-Type", "Authorization", "X-User-Id", "X-User-Role", "X-Admin-Id"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    # Register Centralized Error Handlers
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", "Bad request syntax or invalid parameters")
        return error_response(message=message, status_code=400)

    @app.errorhandler(401)
    def unauthorized(error):
        message = getattr(error, "description", "Unauthorized access")
        return error_response(message=message, status_code=401)

    @app.errorhandler(403)
    def forbidden(error):
        message = getattr(error, "description", "Forbidden access")
        return error_response(message=message, status_code=403)

    @app.errorhandler(404)
    def not_found(error):
        return error_response(message="Requested endpoint or resource was not found", status_code=404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return error_response(message="HTTP method not allowed for this endpoint", status_code=405)

    @app.errorhandler(500)
    def internal_error(error):
        return error_response(message="Internal server error. Please try again later.", status_code=500)

    # Root welcome route
    @app.route("/", methods=["GET"])
    @app.route("/api", methods=["GET"])
    def index():
        return success_response(
            message="Mini E-Commerce API is live and operational!",
            data={
                "project": "Mini E-Commerce Backend",
                "version": "1.0.0",
                "framework": "Flask (Python)",
                "database": "MongoDB Atlas",
                "endpoints": {
                    "health": "/api/health",
                    "auth": {
                        "register": "POST /api/register",
                        "login": "POST /api/login",
                        "profile": "GET /api/profile/<user_id>"
                    },
                    "products": {
                        "all": "GET /api/products",
                        "single": "GET /api/products/<product_id>",
                        "search": "GET /api/products/search?q=<query>",
                        "category": "GET /api/products/category/<category>",
                        "categories": "GET /api/categories"
                    },
                    "cart": {
                        "get": "GET /api/cart/<user_id>",
                        "add": "POST /api/cart",
                        "update": "PUT /api/cart/<user_id>/<product_id>",
                        "remove": "DELETE /api/cart/<user_id>/<product_id>"
                    },
                    "orders": {
                        "checkout": "POST /api/orders",
                        "user_orders": "GET /api/orders/<user_id>",
                        "order_details": "GET /api/orders/<user_id>/<order_id>"
                    },
                    "admin": {
                        "products": "GET/POST /api/admin/products",
                        "product_edit": "PUT/DELETE /api/admin/products/<product_id>",
                        "stock_update": "PATCH /api/admin/products/<product_id>/stock",
                        "orders": "GET /api/admin/orders",
                        "order_status": "PATCH /api/admin/orders/<order_id>/status",
                        "stats": "GET /api/admin/stats"
                    }
                }
            },
            status_code=200
        )

    # Health check route
    @app.route("/api/health", methods=["GET"])
    def health_check():
        db_connected, db_message = test_connection()
        status_code = 200 if db_connected else 503
        return jsonify({
            "success": db_connected,
            "status": "healthy" if db_connected else "degraded",
            "database": {
                "connected": db_connected,
                "message": db_message,
                "db_name": Config.DB_NAME
            }
        }), status_code

    return app


# Application instance
app = create_app()

if __name__ == "__main__":
    print("=" * 60)
    print("  Starting Mini E-Commerce Flask Backend")
    print(f"  Port: {Config.PORT} | Environment: {Config.FLASK_ENV}")
    print("=" * 60)

    # Test MongoDB connection on startup
    connected, conn_msg = test_connection()
    if connected:
        print(f"[Database] {conn_msg}")
        init_db(app)
        # Attempt to auto-seed if empty
        try:
            from seed_data import seed_database
            seed_database(force_refresh=False)
        except Exception as seed_err:
            print(f"[Seed Note] {seed_err}")
    else:
        print(f"[Database Warning] {conn_msg}", file=sys.stderr)
        print("[Database Note] Backend will start, but database requests will fail until MONGO_URI is set.", file=sys.stderr)

    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=Config.DEBUG
    )
