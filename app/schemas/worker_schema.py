from flask_restx import fields
from app import api

worker_model = api.model(
    'worker',
    {
        'client_id': fields.String(required=True, description='Client ID no'),
        'param': fields.String(required=True, description='Task parameters')
    }
)

response_model = api.model(
    'Response',
    {
        'status': fields.String(description='Status of the operations.'),
        'message': fields.String(description='Additional Information.'),
        'data': fields.Raw(description='Optional data payload.')
    }
)