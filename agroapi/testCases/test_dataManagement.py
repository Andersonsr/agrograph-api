import json
from datetime import datetime
from django.test import Client
from django.test import TestCase
from agroapi.model.models import Location, Date, Variable
from neomodel import db, clear_neo4j_database


class testDataManagement(TestCase):
    def setUp(self) -> None:
        clear_neo4j_database(db)
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'name': 'anderson rosa',
            'institution': 'unipampa'
        })
        session = self.client.session
        session['email'] = 'anderson@email.com'
        session['logged'] = 'yes'
        session['uid'] = 'c7f049c2dc8746c6bcc3718730b77967'
        session.save()

    def testInsert(self):
        """check if nodes and relationships are created when /v1/insert/ is requested"""
        data = [
            {
                "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
                "name": "potasio", "unit": "mg/m²", "value": 0.08, "category": "solo"
            },
            {
                "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
                "name": "fosforo", "unit": "mg/m²", "value": 0.91, "category": "solo"
            },
            {
                "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
                "name": "potassium", "unit": "mg/m²", "value": 0.091, "category": "solo"
            },
            {
                "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
                "name": "NDVI", "unit": "ndvi", "value": 1.2, "category": "produção vegetal"
            }
        ]
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(Location.nodes.get_or_none(latitude=0.1, longitude=2.1), None)
        self.assertNotEquals(Date.nodes.get_or_none(date=datetime.strptime('10/02/2021', '%d/%m/%Y')), None)
        self.assertNotEquals(Variable.nodes.get_or_none(name='potasio', unit='mg/m²', value=0.08), None)
        self.assertEquals(1, len(Location.nodes.filter(latitude=-0.1, longitude=-2.1)))
        self.assertEquals(1, len(Location.nodes.filter(latitude=0.1, longitude=2.1)))

    def testRead(self):
        data = [
            {
                "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
                "name": "potasio", "unit": "mg/m²", "value": 0.08, "category": "solo"
            },
            {
                "latitude": 0.1, "longitude": 2.1, "date": "10/02/2021", "time": "10:00:00",
                "name": "fosforo", "unit": "mg/m²", "value": 0.91, "category": "solo"
            },
            {
                "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
                "name": "potassium", "unit": "mg/m²", "value": 0.091, "category": "solo"
            },
            {
                "latitude": -0.1, "longitude": -2.1, "date": "13/02/2021",
                "name": "NDVI", "unit": "ndvi", "value": 1.2, "category": "produção vegetal"
            }
        ]
        self.client.post('/v1/insert/', {"data": json.dumps(data)})

        response = self.client.get('/v1/read/', {})
        print(response.data)
        self.assertEquals(len(json.loads(response.data)), len(data))
