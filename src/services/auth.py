from datetime import datetime, timedelta

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from passlib.hash import bcrypt
from pydantic import ValidationError

from .. import (
    models,
)
from ..settings import settings
from ..db.database import Session, get_session
from ..db import orm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.User:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> models.User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = models.User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: orm.User) -> models.Token:
        user_data = models.User.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat' : now,
            'nbf' : now,
            'exp' : now + timedelta(seconds=settings.jwt_expires_s),
            'sub' : str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return models.Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: models.UserCreate):
        new_user = orm.User(
            login=user_data.login.lower(),
            name=user_data.name,
            password_hash=self.hash_password(user_data.password)
        )
        self.session.add(new_user)
        self.session.commit()
        return self.create_token(new_user)

    def authenticate_user(
            self,
            login: str,
            password: str,
    ) -> models.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
                .query(orm.User)
                .filter(orm.User.login == login)
                .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)