import json

from django.contrib.auth.models import User
from rest_framework import status
from django.test import Client
from django.test import TestCase
from app.model.models import UserProfile
from neomodel import db, clear_neo4j_database
from dotenv import load_dotenv
import os

load_dotenv()
cross_secret = os.environ.get('CROSS_SERVER_SECRET')
data = [
    {
        "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
        "variable": "potasio", "unit": "mg/m²", "value": 0.08, "category": "solo"
    },
    {
        "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
        "variable": "fosforo", "unit": "mg/m²", "value": 0.91, "category": "solo"
    },
    {
        "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
        "variable": "potassium", "unit": "mg/m²", "value": 0.091, "category": "solo"
    },
    {
        "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
        "variable": "NDVI", "unit": "ndvi", "value": 1.2, "category": "produção vegetal"
    }
]


class testUserManagement(TestCase):
    token = ''

    def setUp(self):
        clear_neo4j_database(db)
        self.client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        response = self.client.post('/v1/login/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword'
        })
        self.token = response.json()['token']
        self.client.post('/v1/logout/')

    def testEditProfileAuth(self):
        """test token authentication on edit-profile/"""
        response = self.client.post('/v1/edit-profile/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'name': 'anderson',
            'institution': 'ABC',
            'authToken': self.token,
            'cross_secret': cross_secret
        })

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def testInsertAuth(self):
        """test token authentication on insert/"""

        response = self.client.post('/v1/insert/', {
            "data": json.dumps(data),
            "authToken": self.token,
            "cross_secret": cross_secret
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.post('/v1/insert/', {
            "data": json.dumps(data),
            "cross_secret": cross_secret
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/v1/insert/', {
            "data": json.dumps(data),
            "authToken": self.token,
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/v1/insert/', {
            "data": json.dumps(data),
            "authToken": self.token + '122',
            "cross_secret": cross_secret
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def testMeasurements(self):
        """test token authentication on insert/"""
        response = self.client.get('/v1/measurements/', {
            'authToken': self.token,
            'cross_secret': cross_secret
        })
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/v1/measurements/', {
            'authToken': self.token,
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get('/v1/measurements/', {
            'cross_secret': cross_secret
        })
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
