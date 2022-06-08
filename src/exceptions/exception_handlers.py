from fastapi import Request, status
from fastapi.responses import JSONResponse

from datetime import datetime

from .exceptions import CurrencyRequestException


async def currency_exception_handler(request: Request, exc: CurrencyRequestException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={
            'timestamp': datetime.timestamp(datetime.utcnow()),
            'message'  :  dict(),
            'success'  :  False,
            'error': exc.error
        }
    )