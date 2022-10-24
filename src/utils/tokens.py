from src.schemas.user import User
from jose import jwt
from datetime import timedelta, datetime
from src.core.settings import get_settings
from src.schemas.auth import TokenPayload


settings = get_settings()


def create_access_token(user: User) -> str:
    to_encode = dict(
        id=user.id,
        email=user.email,
        expiration=str(
            datetime.utcnow()
            + timedelta(hours=int(settings.ACCESS_TOKEN_LIFE_IN_HOURS))
        ),
    )
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenPayload:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
