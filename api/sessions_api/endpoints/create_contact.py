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


@router.post('/create_contact', status_code=200, tags=['contacts'])
def create_contact(contact: schemas.Contacts, session_token: Optional[str] = Cookie(None),
                   db: Session = Depends(database.get_db)):
    session = session_and_ttl_check.session_check(session_token, db)
    if not session_and_ttl_check.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # get user id by session_token from session table,
    user_id = api_models.Sessions.get_session_user_id_by_session_token(session_token, db)

    # add contact fields in table
    api_models.Contacts.add_contact_to_contacts_table(user_id, contact.name, contact.surname, contact.phone,
                                                      contact.email, contact.company, contact.group_name, db)
