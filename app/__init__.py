from flask import Flask
from flask_restx import Api
from app.config import config
from config.celery import initialize_celery


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
    app = Flask(__name__)
    app.config.from_object('config')

    api.init_app(app)

    return app

