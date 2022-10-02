from fastapi import APIRouter, HTTPException, status, Depends, Response
from core import schemas, token_
from db import database
from sqlalchemy.orm import Session
from core.hashing import Hash
from datetime import datetime, timedelta
from api.mock import api_models

router = APIRouter()


@router.post('/login')
def login(request: schemas.Login, response: Response, db: Session = Depends(database.get_db)):
    user = db.query(api_models.Users).filter(api_models.Users.user_name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')

    # create access token
    access_token_expires = timedelta(seconds=token_.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = token_.create_access_token()

    # add token to session table
    new_session = api_models.Sessions(user_id=user.id, token=access_token,
                                      creation_time=datetime.now(), ttl=access_token_expires)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    response.set_cookie(key='session_token', value=access_token)
    return 'access token created'
