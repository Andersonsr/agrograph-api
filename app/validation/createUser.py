from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import User
from app.model.models import UserProfile
from django.core.validators import validate_email


def validate(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = request.POST['name']
        institution = request.POST['institution']
    except KeyError:
        return False, JsonResponse({"message": "email, password, name, institution are required"},
                                   status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(email, str):
        return False, JsonResponse({"message": "email must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(password, str):
        return False, JsonResponse({"message": "password must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(password2, str):
        return False, JsonResponse({"message": "password must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(name, str):
        return False, JsonResponse({"message": "name must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(institution, str):
        return False, JsonResponse({"message": "institution must be string"}, status.HTTP_400_BAD_REQUEST)

    if not validate_email(email):
        return False, JsonResponse({"message": "invalid email"}, status.HTTP_400_BAD_REQUEST)

    if len(password) < 8 or len(password) > 16:
        return False, JsonResponse({"message": "password minimum length is 8 and maximum length is 16"},
                                   status.HTTP_400_BAD_REQUEST)

    if password2 != password:
        return False, JsonResponse({"message": "passwords are different"}, status=status.HTTP_400_BAD_REQUEST)

    if 1 > len(name) > 128:
        return False, JsonResponse({"message": "name maximum length is 128"}, status.HTTP_400_BAD_REQUEST)

    if 1 > len(institution) > 128:
        return False, JsonResponse({"message": "institution maximum length is 128"}, status.HTTP_400_BAD_REQUEST)

    return True, None
