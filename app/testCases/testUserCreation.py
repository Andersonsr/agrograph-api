from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from app.model.models import UserProfile
from neomodel import db, clear_neo4j_database


class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        clear_neo4j_database(db)

    def test_create_user_success(self):
        """
        Test creating a new user with valid data.
        """
        url = '/v1/sing-in/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'institution': 'Test Institution'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], 'User created successfully.')

        # Verify that the user and profile are created in the database
        self.assertTrue(User.objects.filter(username='test@example.com').exists())
        self.assertIsNotNone(UserProfile.nodes.first_or_none(email='test@example.com'))

    def test_create_user_missing_fields(self):
        """
        Test creating a new user with missing required fields.
        """
        url = '/v1/sing-in/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            # Missing 'password2', 'name', and 'institution'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Email, password, name, and institution are required.')

        # Verify that the user and profile are not created in the database
        self.assertFalse(User.objects.filter(username='test@example.com').exists())
        self.assertIsNotNone(UserProfile.nodes.first_or_none(email='test@example.com'))

    def test_create_user_password_mismatch(self):
        """
        Test creating a new user with mismatching passwords.
        """
        url = '/v1/sing-in/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'mismatchedpassword',
            'name': 'Test User',
            'institution': 'Test Institution'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Passwords do not match.')

        # Verify that the user and profile are not created in the database
        self.assertFalse(User.objects.filter(username='test@example.com').exists())
        self.assertIsNotNone(UserProfile.nodes.first_or_none(email='test@example.com'))

    def test_create_user_existing_email(self):
        """
        Test creating a new user with an email that already exists.
        """
        # Create a user with the same email
        User.objects.create_user(username='test@example.com', password='testpassword')

        url = '/v1/sing-in/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'institution': 'Test Institution'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.json()['message'], 'This email is already registered.')

        # Verify that the user and profile are not created again in the database
        self.assertTrue(User.objects.filter(username='test@example.com').exists())
        self.assertIsNotNone(UserProfile.nodes.first_or_none(email='test@example.com'))
