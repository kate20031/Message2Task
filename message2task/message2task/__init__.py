# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# # Initialize the database
# db = SQLAlchemy()

# def create_app():
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     # Import models after initializing db
#     from .models import Message

#     return app


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from dotenv import load_dotenv
# import os

# db = SQLAlchemy()
# migrate = Migrate()

# def create_app():
#     load_dotenv()

#     app = Flask(__name__)
#     app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)
#     migrate.init_app(app, db)

#     from .routes import dashboard, auth, messages, webhook
#     app.register_blueprint(dashboard.bp)
#     app.register_blueprint(auth.bp)
#     app.register_blueprint(messages.bp)
#     app.register_blueprint(webhook.bp)

#     return app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
import logging


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import dashboard_bp, auth_bp, messages_bp, home_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(home_bp)
    print(app.url_map) 


    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error('Internal Server Error: %s', e, exc_info=True)
        return "500 Internal Server Error", 500

    return app
