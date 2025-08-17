from flask_restx import Namespace, Resource
from app import api
from app.schemas import worker_model, response_model
from app.utils import create_response

worker = Namespace(
    name='worker',
    description='Worker trigger related operations'
)

@worker.route('/')
@worker.param('queuename', description='Task queue name identifier.')
class WorkerTaskHandler(Resource):
    """
    Endpoint for celery trigger task.
    """
    @worker.doc('create_task')
    @worker.expect(worker_model, validate=True)
    @worker.marshal_with(response_model)
    def post(self, queuename):
        data = api.payload

        if not data:
            return create_response(
                'Error',
                'No parameter',
                '',
                404
            )
        
        


