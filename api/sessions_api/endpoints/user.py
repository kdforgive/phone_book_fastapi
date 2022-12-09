from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database
from db import api_models
from typing import Optional
from sqlalchemy.orm import Session
import logging
from core import session_and_ttl_check

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/say_hello', status_code=200, tags=['user session'])
def say_hello(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    session = session_and_ttl_check.session_check(session_token, db)
    if not session_and_ttl_check.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    column_name = session['user_id']
    username = api_models.Users.get_user_info_by_column(column_name, db)
    logger.debug('user_name found')
    return f'Hello {username["user_name"]}'
