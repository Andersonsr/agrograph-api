import json
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from ..model.writer import writeMeasurement


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def insert(request):
    try:
        email = request.session['email']
        uid = request.session['uid']
        logged = request.session['logged'] == 'yes'
    except KeyError:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_403_FORBIDDEN)

    if logged:
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
                writeMeasurement(longitude, latitude, name, value, unit, date, time, category, email, uid)
            except IntegrityError:
                return JsonResponse({'message': 'something is wrong with your request'},
                                    status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)

