import json
from django.test import TestCase
from app.model.models import UserProfile
from django.test import Client
from ..utils.filters import filterByDate, filterByLocation
from neomodel import db, clear_neo4j_database
from django.contrib.auth.models import User


class test_filter(TestCase):

    def setUp(self) -> None:
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

        data = [
            {
                "longitude": 2.1, "latitude": 0.1, "date": "10/02/2021", "time": "10:00:00",
                "variable": "potasio", "unit": "mg/m²", "value": 0.08, "category": "solo"
            },
            {
                "longitude": 2.1, "latitude": 0.5, "date": "10/02/2021", "time": "12:00:00",
                "variable": "fosforo", "unit": "mg/m²", "value": 0.91, "category": "solo"
            },
            {
                "longitude": -2.1, "latitude": -0.6, "date": "13/02/2021",
                "variable": "potassium", "unit": "mg/m²", "value": 0.091, "category": "solo"
            },
            {
                "longitude": -2.1, "latitude": -0.1, "date": "14/02/2021",
                "variable": "NDVI", "unit": "ndvi", "value": 1.2, "category": "produção vegetal"
            }
        ]
        self.client.post('/v1/insert/', {"data": json.dumps(data)})

    def testLocationFilter(self):
        """unit test for utils.filters.filterByLocation function"""
        user = UserProfile.nodes.first(email='test@example.com')
        measurements = user.measurements.all()

        filterLT3 = [{"latitude": 1, "longitude": 2}, {"latitude": 1, "longitude": 2}]

        filterBigBox = [{"latitude": 3, "longitude": 3},
                        {"latitude": -3, "longitude": 3},
                        {"latitude": 3, "longitude": -3},
                        {"latitude": -3, "longitude": -3}]

        filterSmallTriangle = [{"latitude": 0.3, "longitude": 2.3},
                               {"latitude": -0.1, "longitude": 1.9},
                               {"latitude": -0.1, "longitude": 2.3}]

        self.assertEquals(len(filterByLocation(measurements, None)), 4)
        self.assertEquals(len(filterByLocation(measurements, [None, None, None])), 4)
        self.assertEquals(len(filterByLocation(measurements, [])), 4)
        self.assertEquals(len(filterByLocation(measurements, filterLT3)), 4)
        self.assertEquals(len(filterByLocation(measurements, filterBigBox)), 4)
        self.assertEquals(len(filterByLocation(measurements, filterSmallTriangle)), 1)

    def testDateFilter(self):
        """unit test for utils.filters.filterByDate function"""

        user = UserProfile.nodes.first(email='test@example.com')
        measurements = user.measurements.all()

        self.assertEquals(len(filterByDate(measurements, "10/02/2021", None)), 4)
        self.assertEquals(len(filterByDate(measurements, "12/02/2021", None)), 2)
        self.assertEquals(len(filterByDate(measurements, None, None)), 4)
        self.assertEquals(len(filterByDate(measurements, None, "13/02/2021")), 3)
        self.assertEquals(len(filterByDate(measurements, None, "14/02/2021")), 4)
        self.assertEquals(len(filterByDate(measurements, "10/02/2021", "10/02/2021")), 2)



