from django.db import models
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
    measurements = RelationshipTo('Measurement', 'measurements')


class Location(StructuredNode):
    uid = UniqueIdProperty()
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)


class Date(StructuredNode):
    uid = UniqueIdProperty()
    date = DateTimeFormatProperty(required=True, unique_index=True, format='%d/%m/%Y')


class Variable(StructuredNode):
    categories = {'solo': 1, 'produção vegetal': 2, 'produção animal': 3, 'meteorologia': 4}
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    unit = StringProperty(required=True)
    value = FloatProperty(required=True)
    category = StringProperty(required=True, choices=categories)


class Measurement(StructuredNode):
    time = DateTimeFormatProperty(format='%H:%M:%S')
    uid = UniqueIdProperty()
    resume = StringProperty(required=True)

    # vertices
    where = RelationshipTo('Location', 'where')
    what = RelationshipTo('Variable', 'what')
    when = RelationshipTo('Date', 'when')

