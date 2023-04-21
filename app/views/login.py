from datetime import datetime
from app.utils.hasher import tokenize
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
from app.utils.constants import datetimeFormat
from django.http import JsonResponse
from django.contrib.auth import authenticate
from neomodel.core import DoesNotExist


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse({"message": "something is wrong with your request"},
                            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    try:
        profile = UserProfile.nodes.get(email=email)
    except DoesNotExist:
        return JsonResponse({"message": "wrong user or password"}, status=status.HTTP_401_UNAUTHORIZED)

    if user is not None:
        dateString = datetime.now().strftime(datetimeFormat)
        profile.lastLogin = datetime.strptime(dateString, datetimeFormat)
        profile.lastToken = tokenize(profile.lastLogin.strftime(datetimeFormat), profile.uid)
        profile.save()

        request.session['email'] = email
        request.session['token'] = profile.lastToken
        responseData = {
                        "message": "ok",
                        "token": profile.lastToken,
                        "email": email
                        }
        return JsonResponse(responseData, status=status.HTTP_200_OK)

    else:
        return JsonResponse({"message": "wrong user or password"}, status=status.HTTP_401_UNAUTHORIZED)

    return JsonResponse({"message": "wrong user or password"}, status=status.HTTP_401_UNAUTHORIZED)
