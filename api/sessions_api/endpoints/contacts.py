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


@router.post('/search_in_my_contacts', status_code=200, tags=['contacts'])
def search_in_my_contacts(field: schemas.SelectFields, session_token: Optional[str] = Cookie(None),
                          db: Session = Depends(database.get_db)):
    session = EndpointSessionValidation.session_check(session_token, db)
    if not EndpointSessionValidation.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if field.field_name == 'email' and not EndpointFieldValidation.email_check(field.field_value):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')

    # QUESTION how to do allowed_fields, better with query or simple list ?
    # allowed_fields = ['name', 'surname', 'phone', 'email', 'company', 'group_name']
    # if field not in db this query return empty list, so we can say wrong field data or no field in db
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

    return api_models.Contacts.select_contacts(field.field_name, field.field_value, field.fields_to_show, db)
