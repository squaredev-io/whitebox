from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr
from fastapi.params import Form
from pydantic.fields import Field
from pydantic.networks import HttpUrl


class OAuth2RequestForm:
    def __init__(
        self,
        grant_type: str = Form(None),
        username: Optional[str] = Form(None),
        email: Optional[EmailStr] = Form(None),
        password: Optional[str] = Form(None),
        # scope: str = Form(...),
        # client_id: Optional[str] = Form(None),
        # client_secret: Optional[str] = Form(None),
    ):
        self.grant_type = grant_type
        self.email = username if username else email
        self.password = password
        # self.scope = scope
        # self.client_id = client_id
        # self.client_secret = client_secret


class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenPayload(BaseModel):
#     id: str
#     email: str
#     first_name: str
#     last_name: str
#     username: str
#     expiration: str


# class LoginForm(BaseModel):
#     email: str
#     password: str
#     keepLoggedIn: Optional[bool] = False
#     deviceId: Optional[str] = None


# class LoginResponse(BaseModel):
#     success: bool
#     access_token: Optional[str]
#     userId: Optional[str]
#     error: Optional[str]
