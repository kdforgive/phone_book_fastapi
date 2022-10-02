from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from db import database
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from api.mock import api_models
router = APIRouter()


@router.get('/my_stats', status_code=200)
def my_stats(session_token: Optional[str] = Cookie(None), db: Session = Depends(database.get_db)):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 1 достать из базы данных всю запись сесии по токену(user_id, creation_time, ttl)
    session = db.query(api_models.Sessions).filter(api_models.Sessions.token == session_token).first()
    # 2 если нет такой сейсси 401 ошибка
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # 3 мы должны создать datetime object с финальным валидным верменем(creation_time + ttl)
    ttl = datetime.strptime(session['ttl'],
                            '%H:%M:%S')  # strptime() method creates a datetime object from the given string.
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)  # convert
    date = datetime.strptime(session['creation_time'], "%Y-%m-%d %H:%M:%S")
    datetime_ttl = date + delta  #
    # 4 если сейчас уже больше чем финальное время то 401(подобрать ошибку)
    datetime_current = datetime.now().replace(microsecond=0)
    if datetime_current > datetime_ttl:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # TODO если не валидо надо удалить сессию из таблицы
    # 5 если меньше то сессия валидная

    # 6 используя user_id из таблицы Money данные
    user_stats = db.query(api_models.Money).filter(api_models.Money.id == session['user_id']).first()
    # 7 отправть респонс balance и credit_balance
    return f'balance: {user_stats["balance"]}, credit_balance: {user_stats["credit_balance"]}'
