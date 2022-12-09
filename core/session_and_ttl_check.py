from fastapi import HTTPException, status
from datetime import datetime, timedelta
from db import api_models


def ttl_check(session, session_token, db):
    ttl = datetime.strptime(session['ttl'], '%H:%M:%S')
    delta = timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second)
    date = datetime.strptime(session['creation_time'], "%Y-%m-%d %H:%M:%S.%f")
    datetime_ttl = date + delta
    datetime_current = datetime.now()

    if datetime_current > datetime_ttl:
        api_models.Sessions.delete_session_by_session_token(session_token, db)
        return False
    return True


def session_check(session_token, db):
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    session = api_models.Sessions.get_session_by_session_token(session_token, db)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return session
