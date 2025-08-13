from flask import Flask
from .config import get_config
from .extensions import db, migrate, jwt, swagger
from .resources.auth import auth_bp
from .resources.tasks import tasks_bp


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    @app.get("/")
    def index():
        return {
            "service": "Task Manager API",
            "docs": "/apidocs",
            "version": "1.0.0",
        }

    return app