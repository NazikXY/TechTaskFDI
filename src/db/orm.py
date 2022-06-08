from sqlalchemy import Integer, Column, String, DateTime, DECIMAL

from . import Base, MAX_DATA_LENGTH


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)

    login = Column(String(length=MAX_DATA_LENGTH), nullable=False, unique=True)
    name = Column(String(length=MAX_DATA_LENGTH), nullable=False)
    password_hash = Column(String(length=MAX_DATA_LENGTH), nullable=False)


class CurrencyRate(Base):
    __tablename__ = 'currencies_price'

    id = Column(Integer, primary_key=True, unique=True)

    name = Column(String(length=3))
    datetime = Column(DateTime())
    exchange_rate = Column(DECIMAL())


