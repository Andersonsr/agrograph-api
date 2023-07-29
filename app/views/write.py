import json
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
from django.db import IntegrityError
from app.model.writer import writeMeasurement
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from app.validation.write import validate
from neomodel.core import DoesNotExist
from neomodel.exceptions import MultipleNodesReturned


@api_view(('POST', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@authentication_classes([SessionAuthentication, TokenAuthentication])
def insert(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User authentication failed, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        profile = UserProfile.nodes.get(email=request.user.username)

    except DoesNotExist:
        return JsonResponse({"message": "user does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    except MultipleNodesReturned:
        return JsonResponse({"message": "multiple nodes returned"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    data = json.loads(request.POST.get('data'))

    valid, response = validate(request)
    if not valid:
        return response

    for row in data:
        latitude = row['latitude']
        longitude = row['longitude']
        name = row['variable']
        value = row['value']
        unit = row['unit']
        date = row['date']
        time = row['time'] if 'time' in row else None
        category = row['category']

        try:
            writeMeasurement(longitude, latitude, name, value, unit, date, time, category, profile.uid)

        except IntegrityError:
            return JsonResponse({'message': 'something is wrong with your request'},
                                status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)


