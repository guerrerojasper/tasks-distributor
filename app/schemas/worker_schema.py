from flask_restx import fields
from app import api

worker_model = api.Model(
    'worker',
    {
        'module01': fields.String(required=True, description='Task module01'),
        'module02': fields.String(required=True, description='Task module02'),
        'module03': fields.String(description='Task module03'),
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