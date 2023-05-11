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
from app.validation.read import validate


@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def read(request):
    uid = checkLogin(request)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    valid, response = validate(request)
    if not valid:
        return response

    dateMin = request.GET.get("date-min")
    dateMax = request.GET.get("date-max")
    polygon = request.GET.get("polygon")
    valueMax = request.GET.get("value-max")
    valueMin = request.GET.get("value-min")
    timeMin = request.GET.get("time-min")
    timeMax = request.GET.get("time-max")
    varName = request.GET.get("name")
    category = request.GET.get("category")

    try:
        data = applyALlFilters(uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax,
                               varName, category)
    except KeyError:
        return JsonResponse({'message': 'User has no measurements'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"data": data}, status=status.HTTP_200_OK)
