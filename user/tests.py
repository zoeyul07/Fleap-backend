import json
import bcrypt
import jwt
import re
import unittest

from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock

from fleap.settings import SECRET_KEY
from .models import User


class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="real01@naver.com",
            password="qwer1234!"
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        client = Client()
        user = {
            "email": "test10@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_signup_duplicated_email(self):
        client = Client()
        user = {
            "email": "real01@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'DUPLICATED_KEYS'})

    def test_signup_invalid_keys(self):
        client = Client()
        user = {
            "mail": "test03@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_KEYS'})

    def test_signup_emailerror(self):
        client = Client()
        user = {
            "email": "test03naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)


class SignInTest(TestCase):
    def setUp(self):
        User(
            email='test01@naver.com',
            password=bcrypt.hashpw("qwer1234!".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        ).save()

    def tearDown(self):
        User.objects.all().delete()

    def test_signin_success(self):
        client = Client()
        User = {
            "email": "test01@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        token = jwt.encode({'email': User['email']}, SECRET_KEY, algorithm='HS256').decode('utf-8')
        self.assertEqual(response.json(), {"token": token})

    def test_signin_emailerror(self):
        client = Client()
        User = {
            "email": "test100@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_signin_keyerror(self):
        client = Client()
        User = {
            "mail": "test01@naver.com",
            "password": "qwer1234!"
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signin_passworderror(self):
        client = Client()
        User = {
            "email":  "test01@naver.com",
            "password": "qwer1234@"
        }
        response = client.post('/user/sign-in', json.dumps(User), content_type='application/json')
        self.assertEqual(response.status_code, 401)
