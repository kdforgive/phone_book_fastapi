import random
import logging
from db import api_models
from db import database
from sqlalchemy.orm import Session


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 600

SYMBOLS_SOURCE = f'acdenghijklmopqsuvwxy123456789!#$&*+,-./:<>?@^`|~'

logger = logging.getLogger(__name__)


def create_access_token(length: int = 120, db: Session = next(database.get_db())) -> str:
    token = [random.choice(SYMBOLS_SOURCE) for _ in range(length)]
    attempt = 0
    while True:
        attempt += 1
        if attempt >= 3:
            logger.warning(f'Collision in new access_token creation. Try recreate, attempt number: [{attempt}]')
        if attempt >= 5:
            logger.exception("Couldn't create unique access token")
            raise RuntimeError("Couldn't create unique access token")
        access_token = ''.join(token)
        sessions_count = api_models.Sessions.count_session_by_session_token(access_token, db)
        if sessions_count > 0:
            continue
        break
    return access_token
