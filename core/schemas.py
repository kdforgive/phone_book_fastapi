from pydantic import BaseModel


class User(BaseModel):
    user_name: str
    age: int
    sex: str
    phone_number: str
    password: str


class Money(BaseModel):
    balance: str
    credit_balance: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
