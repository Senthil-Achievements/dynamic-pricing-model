from flask import Flask
from config import Config
from models.database import db, User
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
import os

# Initialize Extensions
login_manager = LoginManager()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    scheduler.init_app(app)

    # Login Manager Settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.api import api_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)

    # CLI Command for Database Initialization
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database initialized")

    # Scheduled Task for Price Updates
    @scheduler.task('interval', id='update_prices_task', seconds=3600) # Every hour
    def scheduled_price_update():
        with app.app_context():
            from utils.pricing_engine import PricingEngine
            engine = PricingEngine()
            engine.update_all_prices()

    if not scheduler.running:
        scheduler.start()

    return app

app = create_app()

if __name__ == '__main__':
    # Ensure static/uploads exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    app.run(debug=True)
