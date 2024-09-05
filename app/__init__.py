from flask import Flask
from app.services.enrollment_scheduler import scheduler

def create_app():
    app = Flask(__name__, static_folder='../static')
    
    # Load configuration
    app.config.from_object('config.Config')

    # Register routes
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    # Start scheduler
    scheduler.start()

    return app
