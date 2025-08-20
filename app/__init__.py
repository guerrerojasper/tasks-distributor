from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from app.config import config
from app.global_init.celery import initialize_celery
from app.global_init.logger import logger
from app.utils import create_response


celery_client = initialize_celery()

# Configure Flask-RESTX API with authorization
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'headers',
        'name': 'X-API-Key'
    },
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: Bearer <your-jwt-token>'
    },
    'jwt-refresh': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Enter: Bearer <refresh-token>'
    }
}

api = Api(
    version='1.0',
    title='Task Distributor APP',
    authorizations=authorizations,
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
    jwt = JWTManager(app)
    api.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_loader(error):
        return create_response('error', 'Missing or Invalid Token', None, 401)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return create_response('error', 'Token has expired', None, 401)

    # Register routes
    from app.register import register_routes
    register_routes()

    logger.info("Flask APP Started...")
    return app

