from fastapi import HTTPException, status
from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, select, text
from sqlalchemy.dialects.mysql import INTEGER


class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(50), unique=False, nullable=False)
    surname = Column(String(50))
    phone = Column(String(20))
    email = Column(String(50))
    company = Column(String(50))
    group_name = Column(String(50), ForeignKey('contact_groups.group_name', ondelete='CASCADE'), default='not assigned')

    groups = relationship('ContactGroups', cascade='all, delete')

    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def add_contact_to_contacts_table(cls, user_id, name, surname, phone, email, company, group_name, db):
        new_session = Contacts(user_id=user_id, name=name, surname=surname, phone=phone, email=email, company=company,
                               group_name=group_name)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)

    @classmethod
    def select_contacts(cls, field_name, field_value, fields_to_show, db):
        """
                field_name: str
                field_value: str
                fields_to_show = ['name', 'surname', 'phone', 'email', 'company', 'group_name']
        """

        all_fields_from_contact_query = db.query(Contacts.name, Contacts.surname, Contacts.phone, Contacts.email,
                                                 Contacts.company, ContactGroups.group_name).join(ContactGroups) \
            .filter(getattr(Contacts, field_name) == field_value).all()

        if not all_fields_from_contact_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'wrong field_name or field_value data '
                                                                              f'or record is missing')
        fields_names = ['name', 'surname', 'phone', 'email', 'company', 'group_name']
        fields_to_show_list = []
        for i in range(len(all_fields_from_contact_query)):
            one_dict_from_response = {}
            fields_to_show_list.append(one_dict_from_response)
            one_dict_from_response.clear()
            for field in fields_to_show:
                if field not in fields_names:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail=f'wrong field_name or field_value data '
                                               f'or record is missing')
                field_in_response = all_fields_from_contact_query[i][field]
                if field in all_fields_from_contact_query[i].keys():
                    one_dict_from_response[field] = field_in_response

        return fields_to_show_list if fields_to_show != [] else all_fields_from_contact_query


class ContactGroups(Base):
    __tablename__ = 'contact_groups'

    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(50), unique=True, nullable=False)

    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get_list_of_contact_groups(cls, db):
        return db.query(ContactGroups.group_id, ContactGroups.group_name).order_by(ContactGroups.group_id)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    age = Column(INTEGER(unsigned=True))
    sex = Column(String(10))
    phone_number = Column(String(20), unique=False, nullable=False)
    password = Column(String(100), unique=True, nullable=False)

    # sessions = relationship("Sessions", back_populates="owner", cascade="all, delete")
    sessions = relationship('Sessions', cascade='all, delete')

    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get_user_info_by_column(cls, column_name, db):
        return db.query(Users).filter(Users.id == column_name).one()

    @classmethod
    def get_user_name(cls, username, db):
        return db.query(Users).filter(Users.user_name == username).first()


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(200), unique=False, nullable=False)
    creation_time = Column(String(50), nullable=False)
    ttl = Column(String(50), nullable=False)

    # owner = relationship("Users", back_populates="items", cascade="all, delete")

    # https://stackoverflow.com/questions/59011757/access-sqlalchemy-class-field-inexplicitly-and-fix-object-is-not-subscriptable
    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get_session_by_session_token(cls, session_token, db):
        return db.query(Sessions).filter(Sessions.token == session_token).first()

    @classmethod
    def get_session_user_id_by_session_token(cls, session_token, db):
        user_id = db.query(Sessions.user_id).filter(Sessions.token == session_token).first()
        return user_id.user_id

    @classmethod
    def delete_session_by_session_token(cls, session_token, db):
        db.query(Sessions).filter(Sessions.token == session_token).delete()
        db.commit()

    @classmethod
    def count_session_by_session_token(cls, session_token, db):
        return db.query(Sessions).filter(Sessions.token == session_token).count()

    @classmethod
    def add_token_to_sessions_table(cls, user_id, access_token, datetime, access_token_expires, db):
        new_session = Sessions(user_id=user_id, token=access_token, creation_time=datetime, ttl=access_token_expires)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
