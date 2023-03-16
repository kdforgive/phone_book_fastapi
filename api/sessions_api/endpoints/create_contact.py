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


@router.post('/create_contact', status_code=200, tags=['contacts'])
def create_contact(contact: schemas.CreateContact, session_token: Optional[str] = Cookie(None),
                   db: Session = Depends(database.get_db)) -> None:

    session = EndpointSessionValidation.session_check(session_token, db)
    if not EndpointSessionValidation.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # get user id by session_token from session table, to pass it to table Contacts for user_id field
    user_id = api_models.Sessions.get_session_user_id_by_session_token(session_token, db)

    if not EndpointFieldValidation.email_check(contact.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='email not correct')
    if contact.name == '' or contact.phone == '':
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if not contact.phone.isnumeric():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='not numeric data in field phone')
    allowed_groups = EndpointFieldValidation.allowed_groups(db)
    if contact.group_name not in allowed_groups:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='group doesn\'t exist')

    # add contact fields in table
    api_models.Contacts.add_contact_to_contacts_table(user_id, contact.name, contact.surname, contact.phone,
                                                      contact.email, contact.company, contact.group_name, db)
