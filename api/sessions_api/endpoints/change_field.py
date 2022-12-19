from fastapi import APIRouter, Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from db import database
from db import api_models
from core import schemas
from core.endpoint_checks import EndpointFieldValidation
from core.endpoint_checks import EndpointSessionValidation
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.put('/change_field', status_code=200, tags=['contacts'])
def change_field(field: schemas.ChangeFields, session_token: Optional[str] = Cookie(None),
                 db: Session = Depends(database.get_db)):
    session = EndpointSessionValidation.session_check(session_token, db)
    if not EndpointSessionValidation.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if field.field_name == 'email' and not EndpointFieldValidation.email_check(field.field_value):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')
    if field.field_name_to_change == 'email' and not EndpointFieldValidation.email_check(field.field_value_to_change):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')

    allowed_fields = EndpointFieldValidation.allowed_fields_check(field.field_name, field.field_value, db,
                                                          field.field_name_to_change)
    if not allowed_fields:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'wrong field_name or field_value data '
                                                                          f'or record is missing')

    if field.field_name == '' or field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == '' and field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    allowed_groups = EndpointFieldValidation.allowed_groups(db)
    if field.field_name_to_change == 'group_name' and field.field_value_to_change not in allowed_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='group doesn\'t exist')

    return api_models.Contacts.update_contact(field.field_name, field.field_value, field.field_name_to_change,
                                              field.field_value_to_change, db)
