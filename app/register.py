from app import api
from app.routes import worker_ns, token_ns
from app.global_init.logger import logger

def register_routes() -> None:
    logger.info("Registering endoints: /v1/")
    api.add_namespace(token_ns, path='/v1/token')
    api.add_namespace(worker_ns, path='/v1/worker')