import json
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.utils.filters import applyALlFilters
from app.utils.checkLogin import checkLogin


@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def read(request):
    email = request.session.get('email')
    token = request.GET.get('authToken')
    secret = request.GET.get('cross_secret')
    uid = checkLogin(email, token, secret)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_400_BAD_REQUEST)

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
        data = applyALlFilters(uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax, varName,
                               category)
    except KeyError:
        return JsonResponse({'message': 'User has no measurements'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return JsonResponse({'message': 'value-max and value-min must be float'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"data": data}, status=status.HTTP_200_OK)
