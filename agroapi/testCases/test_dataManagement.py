from django.contrib.auth.models import User
from rest_framework import status
from django.test import Client
from hashlib import sha256
from django.test import TestCase
from ..models import UserProfile, Location, Date, Measurement, Variable
from neomodel import db, clear_neo4j_database


class testDataManagement(TestCase):
    def setUp(self):
        clear_neo4j_database(db)
        self.client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'name': 'anderson',
            'institution': 'unipampa'
        })
        self.client.post('/v1/login/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword'
        })

    def testInsert(self):
        """check if nodes and relationships are created when /v1/insert/ is used"""
        session = self.client.session
        session['email'] = 'anderson@email.com'
        session.save()
        response = self.client.post('/v1/insert/', {'data': [{'latitude': 0.1, 'longitude': 2.1, 'date': '10/02/2021',
                                                              'time': '10:00:00', 'variable': 'potasio', 'unit': 'mg',
                                                              'value': 0.08}
                                                             ]})
        profile = UserProfile.nodes.get(email='anderson@email.com')
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(Location.nodes.get(latitude=0.1, longitude=2.1), None)
        self.assertNotEquals(Date.nodes.get(date='10/02/2021'), None)
        self.assertNotEquals(Variable.nodes.get(name='potasio', unit='mg', value=0.08), None)
        self.assertNotEquals(Measurement.nodes.get(
            hash=sha256(str(0.1) + str(2.1) + '10/02/2021' + '10:00:00' + profile.uid).digest()), None)

