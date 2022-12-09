from fastapi import APIRouter, Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from db import database
from db import api_models
from core import schemas
from core import session_and_ttl_check
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/search_in_my_contacts', status_code=200, tags=['contacts'])
def search_in_my_contacts(field: schemas.QueryFields, session_token: Optional[str] = Cookie(None),
                          db: Session = Depends(database.get_db)):
    fields_to_show = ['name', 'surname', 'phone', 'email', 'company', 'group_name']
    session = session_and_ttl_check.session_check(session_token, db)
    if not session_and_ttl_check.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if field.field_name == 'phone' and not field.field_value.isnumeric():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='not numeric data in field phone')
    if field.field_name == '' or field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name == '' and field.field_value == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_name not in fields_to_show:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if field.field_value is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    return api_models.Contacts.select_contacts(field.field_name, field.field_value, field.fields_to_show, db)
