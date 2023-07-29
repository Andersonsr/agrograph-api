from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from neomodel.core import DoesNotExist
from neomodel.exceptions import MultipleNodesReturned
from rest_framework.authtoken.models import Token


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login_view(request):
    """
    API endpoint for user login.

    Method: POST

    Parameters:
    - email: User's email (required)
    - password: User's password (required)

    Returns:
    - 200 OK: User authenticated successfully
    - 400 BAD REQUEST: Missing or invalid parameters
    - 401 UNAUTHORIZED: Invalid credentials or user does not exist
    - 500 INTERNAL SERVER ERROR: An error occurred while processing the request
    """
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse({"message": "email and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=email, password=password)

    if user is None:
        return JsonResponse({"message": "wrong user or password"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_profile = UserProfile.nodes.get(email=email)

    except DoesNotExist:
        return JsonResponse({"message": "user does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    except MultipleNodesReturned:
        return JsonResponse({"message": "multiple nodes returned"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    token, created = Token.objects.get_or_create(user=user)
    login(request, user)
    responseData = {
        "message": "ok",
        "token": token.key,
    }
    return JsonResponse(responseData, status=status.HTTP_200_OK)
