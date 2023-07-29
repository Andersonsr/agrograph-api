import json
from datetime import datetime
from django.test import Client
from django.test import TestCase
from app.model.models import Location, Date, Variable, UserProfile, Measurement
from rest_framework import status
from neomodel import db, clear_neo4j_database
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class testWrite(TestCase):
    def setUp(self):
        # clear database
        clear_neo4j_database(db)

        # create user and profile
        user = User.objects.create_user(username='test@example.com', password='testpassword')

        # self.token, created = Token.objects.get_or_create(user=user)
        user_profile = UserProfile(name='Test User', email='test@example.com', institution='Test Institution')
        user_profile.save()

        response = self.client.post('/v1/login/', data={'email': 'test@example.com', 'password': 'testpassword'})
        self.token = response.json()['token']

        # create data
        self.data = [
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

    def test_insert_successful_session(self):
        """check if nodes and relationships are created when /v1/insert/ is requested, session authenticated"""
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})

        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(Location.nodes.get_or_none(latitude=0.1, longitude=2.1), None)
        self.assertNotEquals(Date.nodes.get_or_none(date=datetime.strptime('10/02/2021', '%d/%m/%Y')), None)
        self.assertNotEquals(Variable.nodes.get_or_none(name='potasio', unit='mg/m²', value=0.08), None)
        self.assertEquals(len(Location.nodes.filter(latitude=-0.1, longitude=-2.1)), 1)
        self.assertEquals(len(Location.nodes.filter(latitude=0.1, longitude=2.1)), 1)
        self.assertEquals(len(Variable.nodes.all()), 4)
        self.assertEquals(len(Location.nodes.all()), 2)
        self.assertEquals(len(Date.nodes.all()), 2)

    def test_insert_successful_token(self):
        """check if nodes and relationships are created when /v1/insert/ is requested, token authenticated"""
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + self.token,
        }

        client = Client()
        response = client.post('/v1/insert/', {"data": json.dumps(self.data)}, **auth_headers)

        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(Location.nodes.get_or_none(latitude=0.1, longitude=2.1), None)
        self.assertNotEquals(Date.nodes.get_or_none(date=datetime.strptime('10/02/2021', '%d/%m/%Y')), None)
        self.assertNotEquals(Variable.nodes.get_or_none(name='potasio', unit='mg/m²', value=0.08), None)
        self.assertEquals(1, len(Location.nodes.filter(latitude=-0.1, longitude=-2.1)))
        self.assertEquals(1, len(Location.nodes.filter(latitude=0.1, longitude=2.1)))

    def test_insert_latitude_wrong_type(self):
        """check if invalid latitude value as a string is acceptable"""
        self.data[2]['latitude'] = '-10.0'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no nodes were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

        self.data[2]['latitude'] = -10.0
        self.data[0]['longitude'] = 'abcd'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no nodes were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

    def test_insert_data_different_formats(self):
        """test if different data formats are acceptable"""
        self.data[0]['date'] = '12/31/2023'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.data[1]['date'] = '2023-10-22'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_invalid_category(self):
        """test insertion of non-existing category"""
        self.data[0]['category'] = 'megazord'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

    def test_invalid_date(self):
        """test insertion of invalid date types"""
        self.data[1]['date'] = None
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertIn('format not identified', json.loads(response.content)['message'])

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

        self.data[1]['date'] = '2023-22-10'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json()['message'], 'date format not identified')

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

        self.data[1]['date'] = '20:20:10'
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

    def test_variable_invalid_type(self):
        """test insertion of different invalid variable formats"""
        self.data[2]['variable'] = 2
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)

        self.data[2]['variable'] = None
        response = self.client.post('/v1/insert/', {"data": json.dumps(self.data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        # check if no node were created
        self.assertEquals(len(Measurement.nodes.all()), 0)
        self.assertEquals(len(Variable.nodes.all()), 0)
        self.assertEquals(len(Date.nodes.all()), 0)
        self.assertEquals(len(Location.nodes.all()), 0)
