from fastapi import APIRouter, Depends, HTTPException

from ..services.auth import get_current_user
from ..services.currencies import CurrenciesService

from .. import models

router = APIRouter(prefix='/currencies', tags=['currencies'], dependencies=[Depends(get_current_user)])


@router.get('/get_currencies', response_model=models.CurrencySuccessPair)
async def endpoint(currency_service: CurrenciesService = Depends()):

    usd_result = await currency_service.get_rate('USD')
    eur_result = await currency_service.get_rate('EUR')

    result_model = models.CurrencySuccessPair(
        timestamp=eur_result.timestamp,
        message=models.Pair(
            USD=usd_result.rate,
            EUR=eur_result.rate
        )
    )
    return result_model
