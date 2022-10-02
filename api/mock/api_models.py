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

    # def add_user_if_not_exist()
        # return db.add(new_user)
    #            db.commit()
    #            db.refresh(new_user)


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


class Money(Base):
    __tablename__ = 'money'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(String(50), nullable=False)
    credit_balance = Column(String(50), nullable=False)

    def __getitem__(self, field):
        return self.__dict__[field]
