from rest_framework import status
from django.http import JsonResponse
from app.utils.datetimeConverter import convertDatetime
from app.utils.constants import DATE_FORMAT, TIME_FORMAT
from app.utils.constants import CATEGORIES


def validate(request):
    dateMin = request.GET.get("date-min")
    dateMax = request.GET.get("date-max")
    polygon = request.GET.get("polygon")
    valueMax = request.GET.get("value-max")
    valueMin = request.GET.get("value-min")
    timeMin = request.GET.get("time-min")
    timeMax = request.GET.get("time-max")
    varName = request.GET.get("name")
    category = request.GET.get("category")

    if dateMax is not None:
        dateMax = convertDatetime(dateMax, DATE_FORMAT)
        if dateMax is None:
            return False, JsonResponse({'message': 'dateMax format not identified'},
                                       status=status.HTTP_400_BAD_REQUEST)

    if timeMax is not None:
        timeMax = convertDatetime(timeMax, TIME_FORMAT)
        if timeMax is None:
            return False, JsonResponse({'message': 'timeMax format not identified'},
                                       status=status.HTTP_400_BAD_REQUEST)

    if dateMin is not None:
        dateMin = convertDatetime(dateMin, DATE_FORMAT)
        if dateMin is None:
            return False, JsonResponse({'message': 'dateMin format not identified'},
                                       status=status.HTTP_400_BAD_REQUEST)

    if timeMin is not None:
        timeMin = convertDatetime(timeMin, TIME_FORMAT)
        if not timeMin:
            return False, JsonResponse({'message': 'timeMin format not identified'},
                                       status=status.HTTP_400_BAD_REQUEST)

    if varName is not None and not isinstance(varName, str):
        return False, JsonResponse({'message': 'name must be string'}, status=status.HTTP_400_BAD_REQUEST)

    if category is not None:
        if not isinstance(category, str):
            return False, JsonResponse({'message': 'category must be string'},
                                       status=status.HTTP_400_BAD_REQUEST)

        if category not in CATEGORIES:
            return False, JsonResponse({'message': 'invalid category'}, status=status.HTTP_400_BAD_REQUEST)

    return True, None
