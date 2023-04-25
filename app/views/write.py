import json
from app.utils.checkLogin import checkLogin
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from app.model.writer import writeMeasurement
from app.utils.constants import DATE_FORMAT, TIME_FORMAT
from app.model.models import UserProfile
from app.utils.datetimeConverter import convertDatetime
from neomodel.core import DoesNotExist
from neomodel.exceptions import DeflateError


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    email = request.session.get('email')
    token = request.POST.get('authToken')
    secret = request.POST.get('cross_secret')
    uid = checkLogin(email, token, secret)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    for row in json.loads(request.POST.get('data')):
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

        if not isinstance(value, float) or not isinstance(latitude, float) or not isinstance(longitude, float):
            return JsonResponse({'message': 'value, latitude, longitude must be float type'},
                                status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(name, str) or not isinstance(unit, str) or not isinstance(category, str):
            return JsonResponse({'message': 'name and unit must be string type'},
                                status=status.HTTP_400_BAD_REQUEST)

        newDate = convertDatetime(date, DATE_FORMAT)
        if not newDate:
            return JsonResponse({'message': 'date format not identified'},
                                status=status.HTTP_400_BAD_REQUEST)

        if time is not None:
            newTime = convertDatetime(time, TIME_FORMAT)
            if not newTime:
                return JsonResponse({'message': 'time format not identified'},
                                    status=status.HTTP_400_BAD_REQUEST)

        try:
            writeMeasurement(longitude, latitude, name, value, unit, newDate, newTime, category, uid)
        except IntegrityError:
            return JsonResponse({'message': 'something is wrong with your request'},
                                status=status.HTTP_400_BAD_REQUEST)
        except DeflateError:
            return JsonResponse({'message': 'category not identified'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)


