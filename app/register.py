from app import api
from app.routes import worker_ns

def register_routes() -> None:
    api.add_namespace(worker_ns)