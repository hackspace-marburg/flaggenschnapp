from starlette.responses import JSONResponse


def error_response(msg: str) -> JSONResponse():
    return JSONResponse(dict(error=msg))
