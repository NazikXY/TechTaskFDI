from socket import AF_INET

import aiohttp
import asyncio
from typing import Optional, Any

from ..settings import settings


class SingletonAiohttp:
    sem: Optional[asyncio.Semaphore] = None
    aiohttp_client: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=1)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=settings.SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(base_url=settings.CURRENCY_BASE,
                                                       timeout=timeout,
                                                       connector=connector
                                                       )

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def query_url(cls, url: str, **kwargs) -> Any:
        client = cls.get_aiohttp_client()
        try:
            async with client.get(url, **kwargs) as response:
                if response.status != 200:
                    return await response.json()

                json_result = await response.json()
        except Exception as e:
            return e

        return json_result
