from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app import api
from app.config import config
from app.schemas import response_model
from app.utils import create_response
from app.global_init.logger import logger
from app.global_init.authenticate import require_api_key
from app.schemas import user_model


token_ns = Namespace(
    name='token',
    description='Token request related operations'
)

@token_ns.route('/')
class RequestTokenHandler(Resource):
    """
    Request Token Handler
    """
    @token_ns.doc('get_token', security='apikey')
    @token_ns.expect(user_model, validated=True)
    @token_ns.marshal_with(response_model)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        logger.info("-" * 80)
        logger.info("Resource: RequestTokenHandler")
        logger.info("Method: get_token")
        logger.info(f"Payload: {data}")

        # Validate username and password againts config
        logger.info("Validating username and password")
        if username == config.USER_NAME and password == config.USER_PASSWORD:
            access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRATION))
            refresh_token = create_refresh_token(identity=username, expires_delta=timedelta(days=config.JWT_REFRESH_TOKEN_EXPIRATION))
            logger.info("Access token generated...")
        
        else:
            logger.error("Invalid username or password")
            return create_response('error', 'Invalid username or password', None, 401)

        return create_response('success', '', {'access_token': access_token, 'refresh_token': refresh_token})


@token_ns.route('/refresh')
class RequestTokenResourceHandler(Resource):
    """
    Refresh Token Handler
    """
    @token_ns.doc('refresh_token', security=['apikey', 'jwt-refresh'])
    @token_ns.marshal_with(response_model)
    @require_api_key
    @jwt_required(refresh=True)

    def post(self):
        logger.info("-" * 80)
        logger.info("Resource: RequestTokenResourceHandler")
        logger.info("Method: refresh_token")
        username = get_jwt_identity()
        new_access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRATION))

        logger.info(f"New access token generated for {username}")

        return create_response('success', '', {'access_token': new_access_token}, 200)

