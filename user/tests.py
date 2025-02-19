from django.test import TestCase

from rest_framework.test import APIClient


class UserTestCase(TestCase):
    def setUp(self):
        """setup

        """
        self.client = APIClient()

    def signup(self):
        return self.client.post('/signup/', {"email": "test@test.com", "password": "123"}, format='json')

    def test_signup_success(self):
        """signup with email and password

        """
        resp = self.signup()
        self.assertEqual(resp.status_code, 201)

    def test_signup_failed(self):
        """signup with only email

        """
        resp = self.client.post('/signup/', {"email": "test@test.com"}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_signin(self): # i > u
        """test login successfully

        """
        self.signup()
        resp = self.client.post('/signin/', {"email": "test@test.com", "password": "123"}, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_signin_failed(self):
        """test login failed

        """
        resp = self.client.post('/signin/', {"email": "test@test.com", "password": "1234"}, format='json')
        self.assertEqual(resp.status_code, 400)

    def test_get_me(self):
        """get profile with token

        """
        self.signup()
        resp = self.client.post('/signin/', {"email": "test@test.com", "password": "123"}, format='json')
        resp = self.client.get("/me/", headers={"Authorization": f"Bearer {resp.json()['access_token']}"}, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_get_me_failed(self):
        """get profile without token

        """
        resp = self.client.get("/me/", format='json')
        self.assertEqual(resp.status_code, 401)
