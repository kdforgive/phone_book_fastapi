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


@router.put('/change_field', status_code=200, tags=['contacts'])
def change_field(field: schemas.QueryFields, session_token: Optional[str] = Cookie(None),
                 db: Session = Depends(database.get_db)):
    session = session_and_ttl_check.session_check(session_token, db)
    if not session_and_ttl_check.ttl_check(session, session_token, db):
        logger.info(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

