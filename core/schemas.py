from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class CreateContact(BaseModel):
    name: str = None
    surname: str = None
    phone: str = None
    email: str = None
    company: str = None
    group_name: str = None


class SelectFields(BaseModel):
    field_name: str
    field_value: str
    fields_to_show: list


class ChangeFields(BaseModel):
    field_name: str
    field_value: str
    field_name_to_change: str
    field_value_to_change: str


class DeleteContact(BaseModel):
    field_name: str
    field_value: str
