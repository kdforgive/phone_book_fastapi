from db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.mysql import INTEGER


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(50), unique=True, nullable=False)
    age = Column(INTEGER(unsigned=True))
    sex = Column(String(10))
    phone_number = Column(String(20), unique=False, nullable=False)
    password = Column(String(100), unique=True, nullable=False)

    items = relationship("Sessions", back_populates="owner")

    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get_user_info_by_column(cls, column_name, db):
        return db.query(Users).filter(Users.id == column_name).one()

    @classmethod
    def get_user_name(cls, username, db):
        return db.query(Users).filter(Users.user_name == username).first()

    # def add_user_if_not_exist()
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(200), unique=False, nullable=False)
    creation_time = Column(String(50), nullable=False)
    ttl = Column(String(50), nullable=False)

    owner = relationship("Users", back_populates="items")

    # https://stackoverflow.com/questions/59011757/access-sqlalchemy-class-field-inexplicitly-and-fix-object-is-not-subscriptable
    def __getitem__(self, field):
        return self.__dict__[field]

    @classmethod
    def get_session_by_session_token(cls, session_token, db):
        return db.query(Sessions).filter(Sessions.token == session_token).first()

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


class Money(Base):
    __tablename__ = 'money'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(String(50), nullable=False)
    credit_balance = Column(String(50), nullable=False)

    def __getitem__(self, field):
        return self.__dict__[field]
