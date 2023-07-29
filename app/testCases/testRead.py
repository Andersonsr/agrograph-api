import json
from datetime import datetime
from django.test import Client
from django.test import TestCase
from app.model.models import Location, Date, Variable, UserProfile
from rest_framework import status
from neomodel import db, clear_neo4j_database
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class testDataManagement(TestCase):
    def setUp(self):
        # clear database
        clear_neo4j_database(db)

        # create user and profile
        user = User.objects.create_user(username='test@example.com', password='testpassword')
        user_profile = UserProfile(name='Test User', email='test@example.com', institution='Test Institution')
        user_profile.save()

        response = self.client.post('/v1/login/', data={'email': 'test@example.com', 'password': 'testpassword'})
        token = response.json()['token']

        self.auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + token,
        }

    def testRead(self):
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
        self.client.post('/v1/insert/', {"data": json.dumps(data)}, **self.auth_headers)
        response = self.client.get('/v1/measurements/', {}, **self.auth_headers)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        responseData = response.json()["data"]
        for data in responseData:
            print(data)

        self.assertJSONEqual(json.dumps(responseData), json.dumps(data))



