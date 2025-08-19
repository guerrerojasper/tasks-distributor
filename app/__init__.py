from flask import Flask
from flask_restx import Api
from app.config import config
from app.global_init.celery import initialize_celery
from app.global_init.logger import logger


celery_client = initialize_celery()

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
    logger.info("=" * 80)
    logger.info("Flask APP")
    logger.info("=" * 80)
    logger.info("Initializing Flask APP")
    app = Flask(__name__)
    app.config.from_object(config)

    api.init_app(app)

    # Register routes
    from app.register import register_routes
    register_routes()

    logger.info("Flask APP Started...")
    return app

