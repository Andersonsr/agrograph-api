from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.utils.filters import applyALlFilters
from app.model.models import UserProfile
from app.validation.read import validate
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.decorators import login_required


@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@authentication_classes([SessionAuthentication, TokenAuthentication])
def read(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User authentication failed, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    valid, response = validate(request)
    if not valid:
        return response

    data = request.GET

    dateMin = data.get("date-min")
    dateMax = data.get("date-max")
    polygon = data.get("polygon")
    valueMax = data.get("value-max")
    valueMin = data.get("value-min")
    timeMin = data.get("time-min")
    timeMax = data.get("time-max")
    varName = data.get("name")
    category = data.get("category")

    profile = UserProfile.nodes.get(email=request.user.username)
    try:
        data = applyALlFilters(profile.uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax,
                               varName, category)
    except KeyError:
        return JsonResponse({'message': 'User has no measurements'}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({"data": data}, status=status.HTTP_200_OK)
