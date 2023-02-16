import json
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from ..utils.hasher import hashIt
from django.contrib.auth.models import User
from agroapi.models import UserProfile, Location, Variable, Measurement, Date
from django.contrib.auth import authenticate


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    try:
        email = request.session['email']
        uid = request.session['uid']
        dateFormat = request.POST['date-format']
        logged = request.session['logged'] == 'yes'
    except AttributeError:
        return Response({'message': 'not authorized, login first'}, status=status.HTTP_403_FORBIDDEN)

    if logged:
        profile = UserProfile.nodes.get(email=email)
        nodes = []
        for row in json.loads(request.POST['data']):
            try:
                latitude = row['latitude']
                longitude = row['longitude']
                name = row['name']
                value = row['value']
                unit = row['unit']
                date = row['date']
                if 'time' in row:
                    time = row['time']
                else:
                    time = None
                category = row['category']
            except AttributeError:
                return Response({'message': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                variable = Variable.nodes.get_or_none(name=name, unit=unit, value=value, category=category)
                if variable is None:
                    variable = Variable(name=name, unit=unit, value=value, category=category).save()

                dateObj = Date.nodes.get_or_none(date=datetime.strptime(date, dateFormat))
                if dateObj is None:
                    dateObj = Date(date=datetime.strptime(date, dateFormat)).save()

                location = Location.nodes.get_or_none(latitude=latitude, longitude=longitude)
                if location is None:
                    location = Location(latitude=latitude, longitude=longitude).save()

                newNode = False

                if time is None:
                    measurement = Measurement.nodes.get_or_none(resume=hashIt(date, time, uid, latitude, longitude))

                    if measurement is None:
                        newNode = True
                        measurement = Measurement(resume=hashIt(date, time, uid, latitude, longitude)).save()

                else:
                    measurement = Measurement.nodes.get_or_none(time=datetime.strptime(time, '%H:%M:%S'),
                                                                resume=hashIt(date, time, uid, latitude, longitude))
                    if measurement is None:
                        newNode = True
                        measurement = Measurement(time=datetime.strptime(time, '%H:%M:%S'),
                                                  resume=hashIt(date, time, uid, latitude, longitude)).save()

                if newNode:
                    measurement.who.connect(profile)
                    measurement.where.connect(location)
                    measurement.when.connect(dateObj)
                    measurement.what.connect(variable)
                    measurement.save()

                else:
                    measurement.what.connect(variable)
                    measurement.save()

            except IntegrityError:
                return Response({'message': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def read(request):
    return
