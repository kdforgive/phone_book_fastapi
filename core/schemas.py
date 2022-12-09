from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Contacts(BaseModel):
    name: str
    surname: str
    phone: str
    email: str
    company: str
    group_name: str


class QueryFields(BaseModel):
    field_name: str
    field_value: str
    fields_to_show: list
