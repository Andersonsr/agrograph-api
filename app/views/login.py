from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
from django.http import JsonResponse
from django.contrib.auth import authenticate
from neomodel.core import DoesNotExist
from neomodel.exceptions import MultipleNodesReturned
from rest_framework.authtoken.models import Token


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse({"message": "email and password are required"},
                            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if user is None:
        return JsonResponse({"message": "wrong user or password"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        UserProfile.nodes.get(email=email)

    except DoesNotExist:
        return JsonResponse({"message": "user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    except MultipleNodesReturned:
        return JsonResponse({"message": "multiple nodes returned"}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    request.session['email'] = email
    request.session['token'] = token.key
    responseData = {
                    "message": "ok",
                    "token": token.key,
                    "email": email
                    }
    return JsonResponse(responseData, status=status.HTTP_200_OK)


