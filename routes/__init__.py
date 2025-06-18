from .admin import admin_dashboard_bp
from .auth.registration import registration_bp
from .auth.login import login_bp
from .user_profile import user_profile_bp
from .product import product_bp
from .cart import cart_bp
from .orders import orders_bp

def register_blueprints(app):
    app.register_blueprint(admin_dashboard_bp)
    app.register_blueprint(registration_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(user_profile_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)