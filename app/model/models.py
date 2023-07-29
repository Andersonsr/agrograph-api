from django.db import models
from app.utils.constants import CATEGORIES
from neomodel import StructuredNode, \
                     StringProperty, \
                     UniqueIdProperty, \
                     RelationshipTo, \
                     EmailProperty, \
                     FloatProperty, \
                     DateProperty, \
                     DateTimeFormatProperty
# Create your models here.


class UserProfile(StructuredNode):
    uid = UniqueIdProperty()
    institution = StringProperty(required=True)
    name = StringProperty(required=True)
    email = EmailProperty(required=True, unique_index=True)

    # vertices
    measurements = RelationshipTo('Measurement', 'Measurements')


class Location(StructuredNode):
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)


class Date(StructuredNode):
    date = DateTimeFormatProperty(required=True, unique_index=True, format='%d/%m/%Y')


class Variable(StructuredNode):
    name = StringProperty(required=True)
    unit = StringProperty(required=True)
    value = FloatProperty(required=True)
    category = StringProperty(required=True, choices=CATEGORIES)


class Measurement(StructuredNode):
    time = DateTimeFormatProperty(format='%H:%M:%S')
    hash = StringProperty(required=True)

    # vertices
    location = RelationshipTo('Location', 'Where')
    variables = RelationshipTo('Variable', 'What')
    date = RelationshipTo('Date', 'When')

