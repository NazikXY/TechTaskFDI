from pydantic import BaseSettings


class Settings(BaseSettings):
    SIZE_POOL_AIOHTTP: int = 100
    CURRENCY_BASE: str = 'https://api.apilayer.com'
    CURRENCY_URL: str = '/exchangerates_data/convert'
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    api_key: str

    class Config:
        env_file = '.\src\.env'


settings = Settings()
