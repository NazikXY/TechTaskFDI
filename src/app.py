from datetime import datetime
import traceback

from fastapi import FastAPI, Request, status
from fastapi.responses import PlainTextResponse

from .exceptions import CurrencyRequestException
from .exceptions.exception_handlers import currency_exception_handler

from .api import router as api_router

from . import on_start_up, on_shutdown


app = FastAPI(title='TechTask', version='0.0.1', on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.include_router(api_router)
app.add_exception_handler(CurrencyRequestException, currency_exception_handler)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        return PlainTextResponse(status_code=501, content="Error in function {}:{}".format(traceback.extract_tb(tb=e.__traceback__)[-1] ,e.args))
    return response


