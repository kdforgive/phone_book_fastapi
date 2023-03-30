from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            'example': {
                'username': 'user123',
                'password': 'password123'
            }
        }


class CreateContact(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    group_name: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'name': 'a',
                'phone': '12345',
                'email': 'aa@a.com',
                'group_name': 'family',
                'id': 's_9'
            }
        }


class CreateContactResponse(CreateContact):
    id: str


class SelectFields(BaseModel):
    field_name: str
    field_value: str
    fields_to_show: Optional[list]

    class Config:
        schema_extra = {
            'example': {
                "field_name": "name",
                "field_value": "a",
                "fields_to_show": [
                    "name",
                    "phone",
                    "email",
                    "group_name"
                ]
            }
        }


class ChangeFields(BaseModel):
    field_id: str
    field_name_to_change: str
    field_value_to_change: str

    class Config:
        schema_extra = {
            'example': {
                'field_id': 's_9',
                'field_name_to_change': 'email',
                'field_value_to_change': 'aa@a.com'
            }
        }


class DeleteContact(BaseModel):
    field_name: str
    field_value: str

    class Config:
        schema_extra = {
            'example': {
                'field_name': 'name',
                'field_value': 'd'
            }
        }
