from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from api.mock import api_models

router = APIRouter()


@router.get('/say_hello', status_code=200)
def say_hello(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 1 достать из базы данных всю запись сесии по токену(user_id, creation_time, ttl)
    session = db.query(api_models.Sessions).filter(api_models.Sessions.token == session_token).first()  # TODO убедиться что нет коллизий, если они могут быть надо сделать так что бы их не было
    # 2 если нет такой сейсси 401 ошибка
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 3 мы должны создать datetime object с финальным валидным верменем(creation_time + ttl)
    ttl = datetime.strptime(session['ttl'],
                            '%H:%M:%S')  # strptime() method creates a datetime object from the given string.
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)  # creates timedelta object
    date = datetime.strptime(session['creation_time'],
                             "%Y-%m-%d %H:%M:%S.%f")  # convert creation_time to datetime object
    datetime_ttl = date + delta
    # 4 если сейчас уже больше чем финальное время то 401(подобрать ошибку)
    datetime_current = datetime.now()
    if datetime_current > datetime_ttl:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 5 если меньше то сессия валидная

    # 6 используя user_id из таблицы Users вытащить user_name
    username = db.query(api_models.Users).filter(api_models.Users.id == session['user_id']).first()
    # 7 отправть респонс Hello user_name
    return f'Hello {username["user_name"]}', date, datetime_ttl, datetime_current
