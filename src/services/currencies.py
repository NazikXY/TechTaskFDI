import asyncio.exceptions
from datetime import datetime

from fastapi import Depends, HTTPException, status

from ..db.orm import CurrencyRate
from ..exceptions import CurrencyRequestException
from ..models import CurrencySuccessSingle
from .. import SingletonAiohttp
from ..settings import settings
from ..db.database import get_session, Session


class CurrenciesService:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def write_new_entry(self, result: CurrencySuccessSingle):
        new_entry = CurrencyRate(
            name=result.name,
            datetime=datetime.utcnow(),
            exchange_rate=result.rate
        )
        self._session.add(new_entry)
        self._session.commit()
        ...

    async def get_rate(self, symbol) -> CurrencySuccessSingle:
        eur_params = {
            'amount': 1,
            'from'  : symbol,
            'to'    : 'UAH'
        }
        headers = {
            'apikey' : settings.api_key,
            'Accepts': 'application/json',
        }

        result = await SingletonAiohttp.query_url(settings.CURRENCY_URL, params=eur_params, headers=headers)
        if isinstance(result, asyncio.exceptions.TimeoutError):
            return self.get_last_rate(symbol)
        elif result.get('error'):
            raise CurrencyRequestException(error=result['error'])

        result = CurrencySuccessSingle(
            name=symbol,
            timestamp=result['info']['timestamp'],
            rate=result['result']
        )

        self.write_new_entry(result)

        return result

    def get_last_rate(self, symbol: str) -> CurrencySuccessSingle:
        db_result: CurrencyRate = (
            self._session.query(CurrencyRate)
                .order_by(CurrencyRate.datetime.desc())
                .filter(CurrencyRate.name == symbol)
                .first()
        )
        if not db_result:
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT)
        result = CurrencySuccessSingle(
            timestamp=datetime.timestamp(db_result.datetime),
            name=db_result.name,
            rate=db_result.exchange_rate
        )
        return result


