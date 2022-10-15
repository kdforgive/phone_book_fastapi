from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database, api_models
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter()


@router.get('/my_stats', status_code=200)
def my_stats(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 1 достать из базы данных всю запись сесии по токену(user_id, creation_time, ttl)
    # TODO убедиться что нет коллизий, если они могут быть надо сделать так что бы их не было
    session = db.query(api_models.Sessions).filter(api_models.Sessions.token == session_token).all()
    if len(session) > 1:
        db.query(api_models.Sessions).filter(api_models.Sessions.token == session_token).delete()
        db.commit()
        return 'record with this token already exist, all occurrences was deleted'
    # 2 если нет такой сейсси 401 ошибка
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 3 мы должны создать datetime object с финальным валидным верменем(creation_time + ttl)
    # strptime() method creates a datetime object from the given string.
    ttl = datetime.strptime(session[0]['ttl'], '%H:%M:%S')
    # creates timedelta object
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)
    # convert creation_time to datetime object
    date = datetime.strptime(session[0]['creation_time'], "%Y-%m-%d %H:%M:%S.%f")
    datetime_ttl = date + delta
    # 4 если сейчас уже больше чем финальное время то 401(подобрать ошибку), если меньше то сессия валидная
    datetime_current = datetime.now()
    if datetime_current > datetime_ttl:
        # TODO если не валидо надо удалить сессию из таблицы
        db.query(api_models.Sessions).filter(api_models.Sessions.token == session_token).delete()
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 6 используя user_id из таблицы Money данные
    user_stats = db.query(api_models.Money).filter(api_models.Money.id == session[0]['user_id']).first()
    # 7 отправть респонс balance и credit_balance
    return f'balance: {user_stats["balance"]}, credit_balance: {user_stats["credit_balance"]}'
