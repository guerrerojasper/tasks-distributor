from flask_restx import Namespace, Resource
from app import api, celery_client
from app.schemas import worker_model, response_model
from app.utils import create_response
from app.config import config
from ast import literal_eval


worker_ns = Namespace(
    name='worker',
    description='Worker trigger related operations'
)

# TODO: Add status checking for queued tasks here

@worker_ns.route('/<string:queuename>')
@worker_ns.param('queuename', description='Task queue name identifier.')
class WorkerTaskHandler(Resource):
    """
    Endpoint for celery trigger task.
    """
    @worker_ns.doc('create_task')
    @worker_ns.expect(worker_model, validate=True)
    @worker_ns.marshal_with(response_model)
    def post(self, queuename):
        data = api.payload

        if not data:
            return create_response(
                'Error',
                'No parameter',
                '',
                400
            )
        task_name = data['task_name']
        client_id = data['client_id']
        param = data['param']
        
        if task_name not in config.ALLOWED_TASKS:
            return create_response(
                'Error',
                f'Invalid task name: {task_name}',
                '',
                400
            )
        
        queue = config.ALLOWED_TASKS[task_name]
        print(queue)
        print(task_name),
        print(param)
        param_data = literal_eval(param)
        # Trigger task 
        result = celery_client.send_task(
            task_name,
            kwargs={'x': param_data.get('x'), 'y': param_data.get('y')},
            queue=queue
        )

        return create_response(
            'Finished',
            f'Task {task_name} queued for client {client_id}',
            f'Task ID: {result.id}',
            202
        )


