import json
from rest_framework import status
from django.http import JsonResponse
from app.utils.constants import DATE_FORMAT, TIME_FORMAT
from app.utils.datetimeConverter import convertDatetime
from app.utils.constants import CATEGORIES


def validate(request):
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
            return False, JsonResponse({'message': 'longitude, latitude, variable, value, unit, date are required'},
                                       status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(value, float) or not isinstance(latitude, float) or not isinstance(longitude, float):
            return False, JsonResponse({'message': 'value, latitude, longitude must be float type'},
                                       status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(name, str) or not isinstance(unit, str) or not isinstance(category, str):
            return False, JsonResponse({'message': 'name and unit must be string type'},
                                       status=status.HTTP_400_BAD_REQUEST)

        newDate = convertDatetime(date, DATE_FORMAT)
        if newDate is None:
            return False, JsonResponse({'message': 'date format not identified'},
                                       status=status.HTTP_400_BAD_REQUEST)

        if time is not None:
            newTime = convertDatetime(time, TIME_FORMAT)
            if newTime is None:
                return False, JsonResponse({'message': 'time format not identified'},
                                           status=status.HTTP_400_BAD_REQUEST)
        if category not in CATEGORIES:
            return False, JsonResponse({'message': 'invalid category'}, status=status.HTTP_400_BAD_REQUEST)

    return True, None
