from app.config import config
from functools import wraps
from flask import request, abort
from typing import Callable, Any

def require_api_key(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to validate the API Key againts the config file.
    Args:
        func(callable): The function that will be decorated
    
    Returns:
        func(callable): The wrapped function with API Key validation
    
    Raises:
        HTTPException: Aborts with 401 status if API Key is invalid or missing
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        expected_api_key = config.SECRET_KEY

        if not expected_api_key:
            abort(500, description='Server configuration error: API Key is not found.')
        
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == expected_api_key:
            return func(*args, **kwargs)

        else:
            abort(401, description='Invalid API Key')
    
    return wrapper
