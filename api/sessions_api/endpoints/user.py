from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database, api_models
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get('/say_hello', status_code=200)
def say_hello(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session = api_models.Sessions.get_session_by_session_token(session_token, db)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    ttl = datetime.strptime(session['ttl'], '%H:%M:%S')
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)
    date = datetime.strptime(session['creation_time'], "%Y-%m-%d %H:%M:%S.%f")
    datetime_ttl = date + delta
    datetime_current = datetime.now()

    if datetime_current > datetime_ttl:
        api_models.Sessions.delete_session_by_session_token(session_token, db)
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    column_name = session['user_id']
    username = api_models.Users.get_user_info_by_column(column_name, db)
    logger.debug('user_name found')
    return f'Hello {username["user_name"]}'
