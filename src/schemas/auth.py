from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi.params import Form


class OAuth2RequestForm:
    def __init__(
        self,
        grant_type: str = Form(None),
        email: Optional[EmailStr] = Form(None),
        password: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    id: str
    name: str
    email: str


class LoginForm(BaseModel):
    email: str
    password: str
