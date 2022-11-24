from fastapi.testclient import TestClient
import unittest
from main import app
import json
import mysql.connector
from core.hashing import Hash
from datetime import datetime

client = TestClient(app)
#  https://stackoverflow.com/questions/69166262/fastapi-adding-route-prefix-to-testclient


db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='fastapi_homework1'
)

mycursor = db.cursor()
mycursor.execute('USE fastapi_homework1')


class TestEndpointLogin(unittest.TestCase):
    # TODO вынести в отдельный конфигурационный файл json, в методе setUpClass (time 35:00)
    response_not_valid = {
        "detail": "Incorrect username or password"
    }

    response_empty_username = {
        "detail": [
            {
                "loc": ["body", "username"],
                "msg": "none is not an allowed value",
                "type": "type_error.none.not_allowed"
            }
        ]
    }

    response_empty_password = {
        'detail': [
            {
                'loc': ['body', 'password'],
                'msg': 'none is not an allowed value',
                'type': 'type_error.none.not_allowed'
            }
        ]
    }

    response_empty_password_and_username = {
        'detail': [
            {
                'loc': ['body', 'username'],
                'msg': 'none is not an allowed value', 'type': 'type_error.none.not_allowed'
            },
            {
                'loc': ['body', 'password'],
                'msg': 'none is not an allowed value',
                'type': 'type_error.none.not_allowed'
            }
        ]
    }

    @classmethod
    def setUpClass(cls):
        mycursor.execute(f"INSERT INTO users(id, user_name, age, sex, phone_number, password)"
                         f"VALUES(-1, 'test_user', 88, 'male', 333222111, '{Hash.bcrypt('test_password')}')")
        mycursor.execute(f"INSERT INTO sessions(user_id, token, creation_time, ttl)"
                         f"VALUES(-1, 'abc', '{datetime.now()}', '00:02:00')")
        db.commit()

    @classmethod
    def tearDownClass(cls):
        mycursor.execute(f"DELETE FROM sessions WHERE user_id=-1")
        mycursor.execute(f"DELETE FROM users WHERE id=-1")
        db.commit()

    def test_endpoint_login_200(self):
        data = {"username": "test_user", "password": "test_password"}
        response = client.post('/v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.cookies.get('session_token'))

    def test_endpoint_login_incorrect_username(self):
        data = {"username": "usr", "password": "password"}
        response = client.post('/v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), self.response_not_valid)

    def test_endpoint_login_incorrect_password(self):
        data = {"username": "user1", "password": "passwd"}
        response = client.post('/v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), self.response_not_valid)

    def test_endpoint_login_response_empty_username(self):
        data = {"username": None, "password": "string"}
        response = client.post('v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), self.response_empty_username)

    def test_endpoint_login_response_empty_password(self):
        data = {"username": 'user1', "password": None}
        response = client.post('v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), self.response_empty_password)

    def test_endpoint_login_response_empty_username_and_password(self):
        data = {"username": None, "password": None}
        response = client.post('v1/login', json.dumps(data))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), self.response_empty_password_and_username)
