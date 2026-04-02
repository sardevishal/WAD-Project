import os
from flask import Flask
from .extensions import mongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    # Use explicit absolute or relative paths to the frontend folders
    app = Flask(__name__, 
                static_folder='../../frontend/static', 
                template_folder='../../frontend/templates')
    
    # App configuration (Load from environment variables)
    app.secret_key = os.environ.get('SECRET_KEY', 'default-random-key')
    app.config["MONGO_URI"] = os.environ.get('MONGODB_URI', "mongodb://localhost:27017/study_portal")
    
    # Initialize extension with app
    mongo.init_app(app)
    
    # Production Security (HTTPS & Headers)
    if os.environ.get('FLASK_DEBUG', 'false').lower() == 'false':
        try:
            from flask_talisman import Talisman
            Talisman(app, content_security_policy=None) # CSP set to None for simpler GridFS loading
        except ImportError:
            pass

    # Register blueprint with app
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
