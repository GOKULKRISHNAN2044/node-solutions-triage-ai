from fastapi.responses import JSONResponse
from models.models import success_response, error_response


def ok(data, message: str = "Success") -> JSONResponse:
    return JSONResponse(status_code=200, content=success_response(data, message))


def bad_request(message: str) -> JSONResponse:
    return JSONResponse(status_code=400, content=error_response("BAD_REQUEST", message, 400))


def server_error(message: str) -> JSONResponse:
    return JSONResponse(status_code=500, content=error_response("INTERNAL_ERROR", message, 500))
