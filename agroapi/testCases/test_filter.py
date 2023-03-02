import json
from django.test import TestCase
from ..models import UserProfile, Location, Date, Measurement, Variable
from django.test import Client
from ..utils.filters import filterByDate, filterByLocation
from neomodel import db, clear_neo4j_database


class test_filter(TestCase):

    def setUp(self) -> None:
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'andersonsr@email.com',
            'password': 'strongpassword',
            'name': 'anderson rosa',
            'institution': 'unipampa'
        })
        session = self.client.session
        session['email'] = 'anderson@email.com'
        session['logged'] = 'yes'
        session['uid'] = 'c7f049c2dc8746c6bcc3718730b77967'
        session.save()
        data = [
            {
                "longitude": 2.1, "latitude": 0.1, "date": "10/02/2021", "time": "10:00:00",
                "name": "potasio", "unit": "mg/m²", "value": 0.08, "category": "solo"
            },
            {
                "longitude": 2.1, "latitude": 0.1, "date": "10/02/2021", "time": "12:00:00",
                "name": "fosforo", "unit": "mg/m²", "value": 0.91, "category": "solo"
            },
            {
                "longitude": -2.1, "latitude": -0.1, "date": "13/02/2021",
                "name": "potassium", "unit": "mg/m²", "value": 0.091, "category": "solo"
            },
            {
                "longitude": -2.1, "latitude": -0.1, "date": "14/02/2021",
                "name": "NDVI", "unit": "ndvi", "value": 1.2, "category": "produção vegetal"
            }
        ]
        self.client.post('/v1/insert/', {"data": json.dumps(data)})

    def testLocationFilter(self):
        """unite test for utils.filters.filterByLocation function"""
        user = UserProfile.nodes.first(email='anderson@email.com', name='anderson')
        measurements = user.measurements.all()

        filterLT3 = [{"latitude": 1, "longitude": 2}, {"latitude": 1, "longitude": 2}]
        filterBigBox = [{"latitude": 3, "longitude": 3},
                        {"latitude": -3, "longitude": 3},
                        {"latitude": 3, "longitude": -3},
                        {"latitude": -3, "longitude": -3}]
        filterSmallTriangle = []

        self.assertEquals(len(filterByLocation(measurements, None)), 4)
        self.assertEquals(len(filterByLocation(measurements, [None, None, None])), 4)
        self.assertEquals(len(filterByLocation(measurements, filterLT3)), 4)
        self.assertEquals(len(filterByLocation(measurements, filterBigBox)), 4)

    def testDateFilter(self):
        """unit test for utils.filters.filterByDate function"""

        user = UserProfile.nodes.first(email='anderson@email.com', name='anderson')
        measurements = user.measurements.all()

        self.assertEquals(len(filterByDate(measurements, "10/02/2021", None)), 4)
        self.assertEquals(len(filterByDate(measurements, "12/02/2021", None)), 2)
        self.assertEquals(len(filterByDate(measurements, None, None)), 4)
        self.assertEquals(len(filterByDate(measurements, None, "13/02/2021")), 3)
        self.assertEquals(len(filterByDate(measurements, None, "14/02/2021")), 4)
        self.assertEquals(len(filterByDate(measurements, "10/02/2021", "10/02/2021")), 2)



