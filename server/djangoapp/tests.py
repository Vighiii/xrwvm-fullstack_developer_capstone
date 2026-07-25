import json

from django.contrib.auth.models import User
from django.test import TestCase


class AuthenticationTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="tester", password="StrongPass123!")

    def test_login_and_logout(self):
        response = self.client.post(
            "/djangoapp/login",
            data=json.dumps({"userName": "tester", "password": "StrongPass123!"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")

        response = self.client.get("/djangoapp/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Logged out")

    def test_registration(self):
        response = self.client.post(
            "/djangoapp/register",
            data=json.dumps(
                {
                    "userName": "newuser",
                    "password": "StrongPass123!",
                    "firstName": "New",
                    "lastName": "User",
                    "email": "newuser@example.com",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "Authenticated")


class ApiTests(TestCase):
    def test_car_models(self):
        response = self.client.get("/djangoapp/get_cars")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()["CarModels"]), 0)

    def test_sentiment(self):
        response = self.client.get("/djangoapp/analyze/Fantastic%20services")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "positive")
