from fastapi import APIRouter, HTTPException, status, Depends, Response
from core import schemas
from core import token_
from db import database
from db import api_models
from sqlalchemy.orm import Session
from core.hashing import Hash
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/login', status_code=200, response_model=None, tags=['user session'])
def login(request: schemas.Login, response: Response, db: Session = Depends(database.get_db)) -> None:
    user = api_models.Users.get_by_user_name(request.username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    access_token_expires = timedelta(seconds=token_.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = token_.create_access_token()
    api_models.Sessions.add_token_to_sessions_table(user.id, access_token, datetime.now(), access_token_expires, db)

    # set cookies
    response.set_cookie(key='session_token', value=access_token)
    logger.info('access token created')
