from fastapi import APIRouter, Depends, HTTPException, Query

from ..services.auth import get_current_user
from ..services.currencies import CurrenciesService

from .. import models

router = APIRouter(prefix='/currencies', tags=['currencies'], dependencies=[Depends(get_current_user)])


@router.get(
    '/get_currencies',
    response_model=models.CurrencySuccessPair,
    description="Returns exchange rate of UAH to EUR and USD"
)
async def endpoint(
        amount: float = Query(default=1, gt=0, ),
        currency_service: CurrenciesService = Depends()
):
    usd_result = await currency_service.get_rate('USD', amount)
    eur_result = await currency_service.get_rate('EUR', amount)

    result_model = models.CurrencySuccessPair(
        timestamp=eur_result.timestamp,
        message=models.Pair(
            USD=usd_result.rate,
            EUR=eur_result.rate
        )
    )
    return result_model
