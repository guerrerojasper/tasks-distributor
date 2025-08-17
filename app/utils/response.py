from typing import Dict

def create_response(status: str, message: str, data: any = None, status_code: int = 200) -> tuple[Dict[str, any], str]:
    """
    Create response
    Args:
        status (str): Status of request
        message (str): Message or details of request
        data (any): Either a str or dict details regarding the request
        status_code (int): Status code of request
    Return:
        Status dictionary and status code
    """
    return {
        'status': status,
        'message': message,
        'data': data
    }, status_code