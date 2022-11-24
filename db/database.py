from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql.connector

SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://root:root@127.0.0.1:3306/fastapi_homework1'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    with SessionLocal() as db:
        yield db
