from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import User
from app.model.models import UserProfile


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def createUser(request):
    """
    API endpoint for creating a new user.

    Method: POST

    Parameters:
    - email: The email of the user (required)
    - password: The password for the user (required)
    - password2: Confirmation of the password (required)
    - name: The name of the user (required)
    - institution: The institution of the user (required)

    Returns:
    - 200 OK: User created successfully
    - 400 BAD REQUEST: Missing or invalid parameters
    - 409 CONFLICT: User with the same email already exists
    - 500 INTERNAL SERVER ERROR: An error occurred while creating the user
    """
    try:
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = request.POST['name']
        institution = request.POST['institution']
    except KeyError:
        return JsonResponse({"message": "Email, password, name, and institution are required."},
                            status=status.HTTP_400_BAD_REQUEST)

    if password2 != password:
        return JsonResponse({"message": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return JsonResponse({"message": "This email is already registered."}, status=status.HTTP_409_CONFLICT)

    try:
        user = User.objects.create_user(username=email, password=password)
        profile = UserProfile(institution=institution, name=name, email=email)
        profile.save()

        return JsonResponse({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return JsonResponse({"message": "An error occurred while creating the user."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
