from django.contrib.auth.models import User
from rest_framework import status
from django.test import Client
from django.test import TestCase
from app.model.models import UserProfile
from neomodel import db, clear_neo4j_database
from dotenv import load_dotenv
import os


class testUserManagement(TestCase):
    def setUp(self):
        clear_neo4j_database(db)

    def testCreateUser(self):
        """check if user object is created when /v1/sing-in/ is requested"""
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })

        try:
            User.objects.get(username__exact='anderson@email.com')
        except User.DoesNotExist:
            self.assertTrue(False, 'user does not exist')
        self.assertTrue(True, 'user exist')

        profile = UserProfile.nodes.get(email='anderson@email.com')
        self.assertEquals(profile.name, 'anderson')

    def testEmailValidation(self):
        """test if an invalid email can be used to create a new user"""
        def call():
            client = Client()
            client.post('/v1/sing-in/', {
                'email': 'anderson@.com',
                'password': 'strongpassword',
                'password2': 'strongpassword',
                'name': 'anderson',
                'institution': 'unipampa'
            })

        self.assertRaises(ValueError, call)

    def testEmailDuplication(self):
        """check if multiple users can have the same email"""
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        response = client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson 2',
            'institution': 'unipampa'
        })
        self.assertTrue(status.is_client_error(response.status_code))

    def testSession(self):
        """check if session variable is created when /v1/login/ is requested"""
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        client.post('/v1/login/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword'
        })
        self.assertEquals(client.session['email'], 'anderson@email.com')

    def testLogout(self):
        """check if session variable is removed when /v1/logout/ is requested"""
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        client.post('/v1/login/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword'
        })
        client.post('/v1/logout/', {})
        self.assertNotIn('email', client.session)

    def testEditUser(self):
        """check if fields are changed when /v1/edit-profile/ is requested"""
        newMail = 'anderson02@email.com'
        newName = 'anderson02'
        newPassword = '654321'
        newInstitution = 'uni'

        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        client.post('/v1/login/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword'
        })
        client.post('/v1/edit-profile/', {
            'email': newMail,
            'name': newName,
            'password': newPassword,
            'institution': newInstitution
        })
        try:
            user = User.objects.get(username=newMail)
        except User.DoesNotExist:
            self.assertTrue(False, 'user not found')

        userProfile = UserProfile.nodes.get(email=newMail)

        self.assertEquals(user.username, newMail)
        self.assertEquals(client.session['email'], newMail)
        self.assertEquals(userProfile.email, newMail)
        self.assertEquals(userProfile.institution, newInstitution)
        self.assertEquals(userProfile.name, newName)

    