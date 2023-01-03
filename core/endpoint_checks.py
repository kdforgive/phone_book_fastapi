from fastapi import HTTPException, status
from datetime import datetime, timedelta
from db import api_models
from core import schemas
import re


class EndpointSessionValidation:

    @staticmethod
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

    @staticmethod
    def session_check(session_token, db):
        if not session_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        session = api_models.Sessions.get_session_by_session_token(session_token, db)
        if not session:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return session


class EndpointFieldValidation:

    @staticmethod
    def email_check(email):
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex_email, email):
            return True
        return False

    @staticmethod
    def allowed_fields_check(field_name, field_value, db, field_name_to_change=None):
        # allowed_fields = ['name', 'surname', 'phone', 'email', 'company', 'group_name']
        # allowed_fields = list(schemas.CreateContact().__dict__.keys())
        allowed_fields = [key for key in schemas.CreateContact().__dict__]
        if field_name not in allowed_fields:
            return False
        if field_name_to_change is not None and field_name_to_change not in allowed_fields:
            return False
        query = db.query(api_models.Contacts.name, api_models.Contacts.surname, api_models.Contacts.phone,
                         api_models.Contacts.email, api_models.Contacts.company, api_models.ContactGroups.group_name)\
            .join(api_models.ContactGroups).filter(getattr(api_models.Contacts, field_name) == field_value).all()
        # if query is empty, because wrong field_value
        if not query:
            return False
        return list(query[0].keys())

    @staticmethod
    def allowed_groups(db):
        query = db.query(api_models.ContactGroups.group_name).all()
        allowed_fields_list = []
        for i in range(len(query)):
            allowed_fields_list.append(query[i]['group_name'])
        return allowed_fields_list
