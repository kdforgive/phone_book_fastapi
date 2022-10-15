from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database, api_models
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

router = APIRouter()

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
# file_handler = logging.FileHandler('user.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# logging.basicConfig(filename='user.log', level=logging.DEBUG,
#                     format='%(asctime)s:%(levelname)s:%(message)s')


@router.get('/say_hello', status_code=200)
def say_hello(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 1 достать из базы данных всю запись сесии по токену(user_id, creation_time, ttl)
    # TODO переделать обращения к базе данных(инкапсулировать запросы к БД внутри классов api_models.Sessions)
    session = api_models.Sessions.get_session_by_session_token(session_token, db)
    if not session:
        logging.debug(f'no session')
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 6 используя user_id из таблицы Users вытащить user_name
    column_name = session['user_id']
    username = api_models.Users.get_user_info_by_column(column_name, db)
    # 7 отправть респонс Hello user_name
    return f'Hello {username["user_name"]}'
