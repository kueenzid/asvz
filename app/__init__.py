from flask import Flask
from app.services.enrollment_scheduler import scheduler, refreshTokenScheduler
from config import Config

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    Config.load_credentials()

    # Register routes
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    # Start scheduler
    scheduler.start()
    refreshTokenScheduler.start()

    return app
