from django.test import TestCase, Client
from rest_framework import status
from django.contrib.auth.models import User
from app.model.models import UserProfile
from neomodel.exceptions import DoesNotExist, MultipleNodesReturned
from neomodel import db, clear_neo4j_database


class EditUserTestCase(TestCase):
    def setUp(self):
        clear_neo4j_database(db)
        self.client = Client()
        self.user = User.objects.create_user(username='test@example.com', password='testpassword')
        self.user_profile = UserProfile(name='Test User', email='test@example.com', institution='Test Institution')
        self.user_profile.save()

    def test_edit_user_success(self):
        data = {
            'newName': 'Updated User',
            'newEmail': 'updated@example.com',
            'newPassword': 'updatedpassword',
            'newInstitution': 'Updated Institution',
        }
        self.client.force_login(self.user)
        response = self.client.post('/v1/edit-profile/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], 'User information updated successfully.')

        updated_profile = UserProfile.nodes.get(email='updated@example.com')
        self.assertEqual(updated_profile.name, 'Updated User')
        self.assertEqual(updated_profile.institution, 'Updated Institution')

        # Check if the session is updated with the new email
        self.assertEqual(self.client.session['email'], 'updated@example.com')

    def test_edit_user_missing_parameters(self):
        # Missing a required parameter
        data = {
            'newName': 'Updated User',
            'newEmail': 'updated@example.com',
            'newPassword': 'updatedpassword',
            # 'newInstitution': Missing 'newInstitution' parameter
        }
        self.client.force_login(self.user)
        response = self.client.post('/v1/edit-profile/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'], 'Missing or invalid parameters.')

        # Check if the user information remains unchanged
        unchanged_profile = UserProfile.nodes.get(email='test@example.com')
        self.assertEqual(unchanged_profile.name, 'Test User')
        self.assertEqual(unchanged_profile.institution, 'Test Institution')

    def test_edit_user_invalid_authentication(self):
        # User not logged in
        data = {
            'newName': 'Updated User',
            'newEmail': 'updated@example.com',
            'newPassword': 'updatedpassword',
            'newInstitution': 'Updated Institution',
        }
        response = self.client.post('/v1/edit-profile/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'Authentication credentials were not provided.')

        # Check if the user information remains unchanged
        unchanged_profile = UserProfile.nodes.get(email='test@example.com')
        self.assertEqual(unchanged_profile.name, 'Test User')
        self.assertEqual(unchanged_profile.institution, 'Test Institution')

    def test_edit_user_email_taken(self):
        # Another user already has the new email
        User.objects.create_user(username='anotheruser@email.com', password='anotherpassword')
        newProfile = UserProfile(name='Test User', email='anotheruser@email.com', institution='Test Institution')
        newProfile.save()

        data = {
            'newName': 'Updated User',
            'newEmail': 'anotheruser@email.com',  # Existing email
            'newPassword': 'updatedpassword',
            'newInstitution': 'Updated Institution',
        }
        self.client.force_login(self.user)
        response = self.client.post('/v1/edit-profile/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['message'], 'Email is already taken by another user.')

        # Check if the user information remains unchanged
        unchanged_profile = UserProfile.nodes.get(email='test@example.com')
        self.assertEqual(unchanged_profile.name, 'Test User')
        self.assertEqual(unchanged_profile.institution, 'Test Institution')

