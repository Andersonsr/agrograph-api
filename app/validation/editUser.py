from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth.models import User
from app.model.models import UserProfile
from app.utils.checkLogin import checkLogin
from neomodel.core import DoesNotExist
from django.core.validators import validate_email


def validate(request):
    try:
        newName = request.POST['name']
        newEmail = request.POST['email']
        newPass = request.POST['password']
        newInst = request.POST['institution']
    except KeyError:
        return JsonResponse({"message": "name, email, password, institution are required"},
                            status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(newName, str):
        return False, JsonResponse({"message": "name must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(newEmail, str):
        return False, JsonResponse({"message": "email must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(newPass, str):
        return False, JsonResponse({"message": "password must be string"}, status.HTTP_400_BAD_REQUEST)

    if not isinstance(newInst, str):
        return False, JsonResponse({"message": "institution must be string"}, status.HTTP_400_BAD_REQUEST)

    if not validate_email(newEmail):
        return False, JsonResponse({"message": "invalid email"}, status.HTTP_400_BAD_REQUEST)

    if len(newPass) < 8 or len(newPass) > 16:
        return False, JsonResponse({"message": "password minimum length is 8 and maximum length is 16"},
                                   status.HTTP_400_BAD_REQUEST)

    if len(newName) > 128:
        return False, JsonResponse({"message": "name maximum length is 128"}, status.HTTP_400_BAD_REQUEST)

    if len(newInst) > 128:
        return False, JsonResponse({"message": "institution maximum length is 128"}, status.HTTP_400_BAD_REQUEST)

    return True, None
