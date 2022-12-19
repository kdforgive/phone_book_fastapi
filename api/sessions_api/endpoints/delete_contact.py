from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core import schemas
from db import database
from typing import Optional
from core.endpoint_checks import EndpointFieldValidation
from core.endpoint_checks import EndpointSessionValidation
from db import api_models
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


@router.delete('/delete_contact', status_code=200, tags=['contacts'])
def delete_contact(field: schemas.DeleteContact, session_token: Optional[str] = Cookie(None),
                   db: Session = Depends(database.get_db)):
    session = EndpointSessionValidation.session_check(session_token, db)
    if not EndpointSessionValidation.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if field.field_name == 'email' and not EndpointFieldValidation.email_check(field.field_value):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')

    allowed_fields = EndpointFieldValidation.allowed_fields_check(field.field_name, field.field_value, db)
    if not allowed_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'wrong field_name or field_value data '
                                                                          f'or record is missing')

    if field.field_name == '' or field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == '' and field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == 'phone' and not field.field_value.isnumeric():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='not numeric data in field phone')

    api_models.Contacts.delete_contact(field.field_name, field.field_value, db)
