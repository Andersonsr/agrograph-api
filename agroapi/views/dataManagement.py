import json
from hashlib import sha256
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from django.contrib.auth.models import User
from agroapi.models import UserProfile, Location, Variable, Measurement, Date
from django.contrib.auth import authenticate


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    try:
        email = request.session['email']
        logged = 'logged' in request.session
    except KeyError:
        return Response({'detail': 'not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if logged:
        profile = UserProfile.nodes.get(email=email)
        try:
            data = request.POST['data']
        except KeyError:
            return Response({'detail': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)

        nodes = []
        for row in data:
            row = json.loads(row)
            try:
                latitude = row.latitude
                longitude = row.longitude
                name = row.variable
                value = row.value
                unit = row.unit
                date = row.date
                time = row.time
            except AttributeError:
                return Response({'detail': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                digest = sha256(str(latitude) + str(longitude) + date + time + profile.uid).digest()
                variable = Variable.get_or_create({'name': name, 'unit': unit, 'value': value})
                dateObj = Date.get_or_create({'date': date})
                location = Location.get_or_create({'latitude': latitude, 'longitude': longitude})
                measurement = Measurement.get_or_create({'time': time, 'hash': digest})
                measurement.who.connect(profile)
                measurement.where.connect(location)
                measurement.when.connect(dateObj)
                measurement.what.connect(variable)
            except IntegrityError:
                return Response({'detail': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)

            nodes.extend([variable, dateObj, location, measurement])

        for node in nodes:
            node.save()
        return Response({'detail': 'ok'}, status=status.HTTP_200_OK)
