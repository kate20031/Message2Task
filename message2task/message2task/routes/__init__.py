from .dashboard import dashboard_bp
from .auth import auth_bp
from .messages import messages_bp

# Якщо у тебе є окремий webhook blueprint:
from .webhook import webhook_bp  # або просто використовуй messages_bp, якщо webhook — частина messages

# Експортуй для create_app
__all__ = ["dashboard_bp", "auth_bp", "messages_bp", "webhook_bp"]
