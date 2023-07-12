import json
from app.utils.checkLogin import checkLogin
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes, permission_classes, authentication_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
from django.db import IntegrityError
from app.model.writer import writeMeasurement
from app.validation.write import validate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def insert(request):
    if request.user is not None:
        data = json.loads(request.POST.get('data'))
        profile = UserProfile.nodes.get(email=request.user.username)

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


