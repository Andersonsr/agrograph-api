from django.test import TestCase, Client
from app.model.models import UserProfile
from rest_framework import status
from django.contrib.auth.models import User
from neomodel import db, clear_neo4j_database


class LoginTestCase(TestCase):
    def setUp(self):
        clear_neo4j_database(db)
        self.client = Client()

    def test_login_successful(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password'
        user = User.objects.create_user(username=email, password=password)
        profile = UserProfile(name='test name', email=email, institution='test institution')
        profile.save()

        # Prepare the login request data
        data = {
            'email': email,
            'password': password
        }

        # Send the login request
        response = self.client.post('/v1/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data
        expected_data = {
            'message': 'ok',
            'token': user.auth_token.key,
        }
        self.assertJSONEqual(response.content, expected_data)

    def test_login_missing_parameters(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password'
        user = User.objects.create_user(username=email, password=password)
        UserProfile(name='test name', email=email, institution='test institution')

        # Prepare the login request data with missing parameters
        data = {
            'email': 'test@example.com'
            # Missing 'password' parameter
        }

        # Send the login request
        response = self.client.post('/v1/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify the response data
        expected_data = {
            'message': 'email and password are required'
        }
        self.assertJSONEqual(response.content, expected_data)

    def test_login_invalid_credentials(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password'
        user = User.objects.create_user(username=email, password=password)
        profile = UserProfile(name='test name', email=email, institution='test institution')
        profile.save()

        # Prepare the login request data with invalid credentials
        data = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }

        # Send the login request
        response = self.client.post('/v1/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify the response data
        expected_data = {
            'message': 'wrong user or password'
        }
        self.assertJSONEqual(response.content, expected_data)

    def test_login_user_not_found(self):
        # Create a test user
        email = 'test@example.com'
        password = 'password'
        user = User.objects.create_user(username=email, password=password)
        profile = UserProfile(name='test name', email=email, institution='test institution')
        profile.save()

        # Prepare the login request data for a non-existing user
        data = {
            'email': 'nonexisting@example.com',
            'password': 'password'
        }

        # Send the login request
        response = self.client.post('/v1/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Verify the response data
        expected_data = {
            'message': 'wrong user or password'
        }
        self.assertJSONEqual(response.content, expected_data)
