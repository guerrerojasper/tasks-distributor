from flask_restx import Namespace, Resource
from app import api, celery_client
from app.schemas import worker_model, response_model
from app.utils import create_response
from app.config import config
from app.global_init.logger import logger
from ast import literal_eval


worker_ns = Namespace(
    name='worker',
    description='Worker trigger related operations'
)

# TODO: Add status checking for queued tasks here

@worker_ns.route('/<string:taskname>')
@worker_ns.param('taskname', description='Task task name identifier.')
class WorkerTaskHandler(Resource):
    """
    Endpoint for celery trigger task.
    """
    @worker_ns.doc('create_task')
    @worker_ns.expect(worker_model, validate=True)
    @worker_ns.marshal_with(response_model)
    def post(self, taskname):
        data = api.payload
        logger.info("-" * 80)
        logger.info("Resource: WorkerTaskHandler")
        logger.info(f"Payload: {data}")
        logger.info(f"Path parameter - taskname: {taskname}")

        if not data:
            logger.error("Error: No Payload 'data'")
            return create_response(
                'Error',
                'No Payload - data',
                '',
                400
            )
        client_id = data['client_id']
        param = data['param']
        
        if taskname not in config.ALLOWED_TASKS:
            logger.error(f"Task name: {taskname} doesn't exist")
            return create_response(
                'Error',
                f'Invalid task name: {taskname}',
                '',
                400
            )
        
        queue = config.ALLOWED_TASKS[taskname]
        param_data = literal_eval(param)
        logger.info(f"Queue name: {queue}")
        # Trigger task 
        result = celery_client.send_task(
            taskname,
            kwargs={'x': param_data.get('x'), 'y': param_data.get('y')},
            queue=queue
        )
        logger.info(f"Task {taskname} queued for client {client_id}")
        logger.info("-" * 80)

        return create_response(
            'Finished',
            f'Task {taskname} queued for client {client_id}',
            f'Task ID: {result.id}',
            202
        )


