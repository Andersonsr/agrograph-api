import json
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.utils.filters import applyALlFilters
from app.utils.checkLogin import checkLogin
from app.utils.datetimeConverter import convertDatetime
from app.utils.constants import DATE_FORMAT, TIME_FORMAT
from app.utils.constants import CATEGORIES

@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def read(request):
    uid = checkLogin(request)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

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
        if not dateMax:
            return JsonResponse({'message': 'dateMax format not identified'},
                                status=status.HTTP_400_BAD_REQUEST)

    if timeMax is not None:
        timeMax = convertDatetime(timeMax, TIME_FORMAT)
        if not timeMax:
            return JsonResponse({'message': 'timeMax format not identified'},
                                status=status.HTTP_400_BAD_REQUEST)

    if dateMin is not None:
        dateMin = convertDatetime(dateMin, DATE_FORMAT)
        if not dateMin:
            return JsonResponse({'message': 'dateMin format not identified'},
                                status=status.HTTP_400_BAD_REQUEST)

    if timeMin is not None:
        timeMin = convertDatetime(timeMin, TIME_FORMAT)
        if not timeMin:
            return JsonResponse({'message': 'timeMin format not identified'},
                                status=status.HTTP_400_BAD_REQUEST)

    if varName is not None and not isinstance(varName, str):
        return JsonResponse({'message': 'name must be string'}, status=status.HTTP_400_BAD_REQUEST)

    if category is not None:
        if not isinstance(category, str):
            return JsonResponse({'message': 'category must be string'}, status=status.HTTP_400_BAD_REQUEST)

        if category not in CATEGORIES:
            return JsonResponse({'message': 'invalid category'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = applyALlFilters(uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax,
                               varName, category)
    except KeyError:
        return JsonResponse({'message': 'User has no measurements'}, status=status.HTTP_400_BAD_REQUEST)

    except ValueError:
        return JsonResponse({'message': 'value-max and value-min must be float'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"data": data}, status=status.HTTP_200_OK)
