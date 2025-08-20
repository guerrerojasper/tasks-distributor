from flask_restx import fields
from app import api

user_model = api.model(
    'user',
    {
        'username': fields.String(required=True, description='Client Username'),
        'password': fields.String(required=True, description='Client Password')
    }
)
