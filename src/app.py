from datetime import datetime

from fastapi import FastAPI, Request, status

from .exceptions import CurrencyRequestException
from .exceptions.exception_handlers import currency_exception_handler

from .api import router as api_router

from . import on_start_up, on_shutdown


app = FastAPI(title='TechTask', version='0.0.1', on_startup=[on_start_up], on_shutdown=[on_shutdown])

app.include_router(api_router)
app.add_exception_handler(CurrencyRequestException, currency_exception_handler)


