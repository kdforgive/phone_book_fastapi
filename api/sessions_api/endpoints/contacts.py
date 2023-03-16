from fastapi import APIRouter, Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from db import database
from db import api_models
from core import schemas
from core.endpoint_checks import EndpointFieldValidation
from core.endpoint_checks import EndpointSessionValidation
from typing import Optional
import logging
from functools import wraps


router = APIRouter()
logger = logging.getLogger(__name__)


# def user_id_validation(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         session = EndpointSessionValidation.session_check(kwargs['session_token'], kwargs['db'])
#         if not EndpointSessionValidation.ttl_check(session, kwargs['session_token'], kwargs['db']):
#             logger.info(f'token has expired')
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#         return func(*args, **kwargs)
#     return wrapper


@router.post('/search_in_my_contacts', status_code=200, response_model=list[schemas.CreateContactResponse], tags=['contacts'])
# @user_id_validation
def search_in_my_contacts(field: schemas.SelectFields, session_token: Optional[str] = Cookie(None),
                          db: Session = Depends(database.get_db)) -> list[schemas.CreateContact]:

    session = EndpointSessionValidation.session_check(session_token, db)
    if not EndpointSessionValidation.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if field.field_name == 'email' and not EndpointFieldValidation.email_check(field.field_value):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')

    # if field not in db this query return empty list, so we can say wrong field data or no field in db
    allowed_fields = EndpointFieldValidation.allowed_fields_check(field.field_name, field.field_value, db)
    if not allowed_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'wrong field_name or field_value data '
                                                                          f'or record is missing')
    # check fields_to_show for correct field names
    allowed_fields_to_show = EndpointFieldValidation.allowed_fields_to_show(field.fields_to_show)
    if not allowed_fields_to_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'wrong field name')

    if field.field_name == '' or field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == '' and field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == 'phone' and not field.field_value.isnumeric():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='not numeric data in field phone')

    return api_models.Contacts.select_contacts(field.field_name, field.field_value, field.fields_to_show, db)
