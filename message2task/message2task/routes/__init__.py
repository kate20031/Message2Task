from .dashboard import dashboard_bp
from .auth import auth_bp
from .messages import messages_bp


# Експортуй для create_app
__all__ = ["dashboard_bp", "auth_bp", "messages_bp", "webhook_bp"]
