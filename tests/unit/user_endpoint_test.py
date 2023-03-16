import unittest
import mysql.connector
from fastapi import APIRouter
from fastapi.testclient import TestClient
from main import app
import mysql.connector
from core.hashing import Hash
from datetime import datetime
import json

router = APIRouter()
client = TestClient(app)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='fastapi_homework1'
)

mycursor = db.cursor()
mycursor.execute('USE fastapi_homework1')


class ResponseTest(unittest.TestCase):

    response_not_valid = {
        'detail': 'Unauthorized'
    }

    @classmethod
    def setUpClass(cls):
        mycursor.execute(f"INSERT INTO users(id, user_name, age, sex, phone_number, password)"
                         f"VALUES(-1, 'test_user', 88, 'male', 333222111, '{Hash.bcrypt('test_password')}')")
        mycursor.execute(f"INSERT INTO sessions(user_id, token, creation_time, ttl)"
                         f"VALUES(-1, 'abc', '{datetime.now()}', '00:02:00')")
        db.commit()
        cls.__user_name = 'test_user'
        cls.__password = "test_password"
        cls._token = cls.get_session_token()

    @classmethod
    def tearDownClass(cls):
        mycursor.execute(f"DELETE FROM sessions WHERE user_id=-1")
        mycursor.execute(f"DELETE FROM users WHERE id=-1")
        db.commit()

    @classmethod
    def get_session_token(cls):
        # TODO вынести юзернейм и псворд в одельные переменные вне метода (time 1:17:20)
        data = {"username": cls.__user_name, "password": cls.__password}
        response = client.post('/v1/login', json.dumps(data))
        client.cookies.clear()
        return response.cookies.get('session_token')

    def test_say_hello_wrong_session_token(self):
        response = client.get('/v1/say_hello')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), self.response_not_valid)

    def test_say_hello_200(self):
        response = client.get('/v1/say_hello', cookies={'session_token': self._token})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.__user_name, response.text)
