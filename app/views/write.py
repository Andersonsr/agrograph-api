import json
from app.utils.checkLogin import checkLogin
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from app.model.writer import writeMeasurement
from app.validation.write import validate
from neomodel.core import DoesNotExist
from neomodel.exceptions import DeflateError


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    uid = checkLogin(request)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    valid, response = validate(request)
    if not valid:
        return response

    for row in json.loads(request.POST.get('data')):
        latitude = row['latitude']
        longitude = row['longitude']
        name = row['variable']
        value = row['value']
        unit = row['unit']
        date = row['date']
        time = row['time'] if 'time' in row else None
        category = row['category']

        try:
            writeMeasurement(longitude, latitude, name, value, unit, date, time, category, uid)
        except IntegrityError:
            return JsonResponse({'message': 'something is wrong with your request'},
                                status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)


