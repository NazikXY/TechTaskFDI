from .connections.connection import SingletonAiohttp


async def on_start_up() -> None:
    SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    await SingletonAiohttp.close_aiohttp_client()
