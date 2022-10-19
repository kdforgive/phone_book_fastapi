from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database, api_models
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging.config
from logs.setup_logging import read_log_config

router = APIRouter()

read_log_config()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
# handler = logging.FileHandler('logs/user.log')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


@router.get('/say_hello', status_code=200)
def say_hello(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 1 достать из базы данных всю запись сесии по токену(user_id, creation_time, ttl)
    # TODO переделать обращения к базе данных(инкапсулировать запросы к БД внутри классов api_models.Sessions)
    session = api_models.Sessions.get_session_by_session_token(session_token, db)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 3 мы должны создать datetime object с финальным валидным верменем(creation_time + ttl)
    # strptime() method creates a datetime object from the given string.
    ttl = datetime.strptime(session['ttl'], '%H:%M:%S')
    # creates timedelta object
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)
    # convert creation_time to datetime object
    date = datetime.strptime(session['creation_time'], "%Y-%m-%d %H:%M:%S.%f")
    datetime_ttl = date + delta
    # 4 если сейчас уже больше чем финальное время то 401(подобрать ошибку), если меньше то сессия валидная
    datetime_current = datetime.now()
    if datetime_current > datetime_ttl:
        # TODO если не валидо надо удалить сессию из таблицы
        api_models.Sessions.delete_session_by_session_token(session_token, db)
        logger.debug(f'token has expired')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 6 используя user_id из таблицы Users вытащить user_name
    column_name = session['user_id']
    username = api_models.Users.get_user_info_by_column(column_name, db)
    # 7 отправть респонс Hello user_name
    logger.debug('get user_name')
    return f'Hello {username["user_name"]}'
