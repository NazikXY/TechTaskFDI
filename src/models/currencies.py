from datetime import datetime

from pydantic import BaseModel


class Pair(BaseModel):
    USD: float
    EUR: float


class CurrencySuccessBase(BaseModel):
    success: bool = True
    timestamp: datetime


class CurrencySuccessSingle(CurrencySuccessBase):
    name: str
    rate: float


class CurrencySuccessPair(CurrencySuccessBase):
    message: Pair


class ErrorMessage(BaseModel):
    code: str
    message: str


class CurrencyErrorResponse(BaseModel):
    timestamp: datetime
    message: dict = {}
    success: bool = False
    error: ErrorMessage


