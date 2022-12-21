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


class Location(StructuredNode):
    uid = UniqueIdProperty()
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)


class Date(StructuredNode):
    uid = UniqueIdProperty()
    date = DateProperty(required=True, unique_index=True)


class Variable(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    unit = StringProperty(required=True)
    value = FloatProperty(required=True)


class Measurement(StructuredNode):
    time = DateTimeFormatProperty(format='%HH:%mm:%ss')
    uid = UniqueIdProperty()
    hash = StringProperty(unique_index=True)

    # relations
    where = RelationshipTo('Location', 'where')
    who = RelationshipTo('UserProfile', 'who')
    what = RelationshipTo('Variable', 'what')
    when = RelationshipTo('Date', 'when')

