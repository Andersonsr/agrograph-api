import json
from datetime import datetime
from app.utils.checkLogin import checkLogin
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from ..model.writer import writeMeasurement
from app.model.models import UserProfile
from neomodel.core import DoesNotExist


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    email = request.session.get('email')
    token = request.POST.get('authToken')
    secret = request.POST.get('cross_secret')
    uid = checkLogin(email, token, secret)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    for row in json.loads(request.POST['data']):
        try:
            latitude = row['latitude']
            longitude = row['longitude']
            name = row['variable']
            value = row['value']
            unit = row['unit']
            date = row['date']
            time = row['time'] if 'time' in row else None
            category = row['category']
        except KeyError:
            return JsonResponse({'message': 'longitude, latitude, variable, value, unit, date are required'},
                                status=status.HTTP_400_BAD_REQUEST)
        try:
            writeMeasurement(longitude, latitude, name, value, unit, date, time, category, uid)
        except IntegrityError:
            return JsonResponse({'message': 'something is wrong with your request'},
                                status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)

