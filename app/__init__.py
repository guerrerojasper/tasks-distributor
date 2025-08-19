from flask import Flask
from flask_restx import Api
from app.config import config
from app.global_init.celery import initialize_celery


celery_client = initialize_celery()
print(f"Backend object: {celery_client.backend}")


api = Api(
    version='1.0',
    title='Task Distributor APP',
    description='A simple Flask APP for task distributing celery worker',
    doc='/swagger'
)

def create_app() -> Flask:
    """
    Flask APP initialization
    Args:
        None
    Return:
        Flask APP
    """
    app = Flask(__name__)
    app.config.from_object(config)

    api.init_app(app)

    # Register routes
    from app.register import register_routes
    register_routes()

    return app

