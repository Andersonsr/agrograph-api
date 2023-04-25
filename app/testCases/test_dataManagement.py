import json
from datetime import datetime
from django.test import Client
from django.test import TestCase
from app.model.models import Location, Date, Variable
from rest_framework import status
from neomodel import db, clear_neo4j_database


class testDataManagement(TestCase):
    def setUp(self) -> None:
        clear_neo4j_database(db)
        client = Client()
        client.post('/v1/sing-in/', {
            'email': 'anderson@email.com',
            'password': 'strongpassword',
            'password2': 'strongpassword',
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
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, 200)
        self.assertNotEquals(Location.nodes.get_or_none(latitude=0.1, longitude=2.1), None)
        self.assertNotEquals(Date.nodes.get_or_none(date=datetime.strptime('10/02/2021', '%d/%m/%Y')), None)
        self.assertNotEquals(Variable.nodes.get_or_none(name='potasio', unit='mg/m²', value=0.08), None)
        self.assertEquals(1, len(Location.nodes.filter(latitude=-0.1, longitude=-2.1)))
        self.assertEquals(1, len(Location.nodes.filter(latitude=0.1, longitude=2.1)))

        data[0]['date'] = '12/02/2023'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        data[1]['date'] = None
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertIn('format not identified', json.loads(response.content)['message'])

        data[1]['date'] = '2023-10-10'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        data[1]['date'] = '20:20:10'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        data[0]['latitude'] = 'abcd'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        data[0]['latitude'] = '-10.0'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        data[0]['latitude'] = 10.0
        data[0]['category'] = 'sem categoria'
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        data[0]['category'] = 'solo'
        data[2]['variable'] = 2
        response = self.client.post('/v1/insert/', {"data": json.dumps(data)})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        self.client.post('/v1/insert/', {"data": json.dumps(data)})
        response = self.client.get('/v1/measurements/', {})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        responseData = json.loads(response.content)["data"]
        self.assertEquals(len(responseData), len(data))
        self.assertIn("latitude", data[0])
        self.assertIn("longitude", data[0])
        self.assertIn("variable", data[0])
        self.assertIn("unit", data[0])
        self.assertIn("category", data[0])
        self.assertIn("date", data[0])

        response = self.client.get('/v1/measurements/', {"name": "fosforo"})
        self.assertEquals(len(json.loads(response.content)["data"]), 1)

        response = self.client.get('/v1/measurements/', {"name": "fosforo potassium"})
        self.assertEquals(len(json.loads(response.content)["data"]), 2)

        response = self.client.get('/v1/measurements/', {"name": ['fosforo potassium']})
        self.assertEquals(len(json.loads(response.content)["data"]), 2)

        response = self.client.get('/v1/measurements/', {"name": ''})
        self.assertEquals(len(json.loads(response.content)["data"]), 0)

        response = self.client.get('/v1/measurements/', {"name": "fosforo potassium", 'value-min': 0.9})
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(response.content)["data"]), 1)

        response = self.client.get('/v1/measurements/', {"value-min": 0.5, 'value-max': 1})
        self.assertEquals(len(json.loads(response.content)["data"]), 1)

        response = self.client.get('/v1/measurements/', {"value-min": 0.5, 'value-max': ''})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/v1/measurements/', {"value-min": 'a', 'value-max': ''})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/v1/measurements/', {'value-max': ''})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/v1/measurements/', {"category": 'a'})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get('/v1/measurements/', {"category": 'produção vegetal'})
        self.assertEquals(len(json.loads(response.content)["data"]), 1)



