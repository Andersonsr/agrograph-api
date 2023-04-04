from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from app.model.models import UserProfile
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
        return JsonResponse({"message": "user not found"}, status=status.HTTP_401_UNAUTHORIZED)

    if user is not None:
        request.session['email'] = email
        request.session['logged'] = 'yes'
        request.session['uid'] = profile.uid
        return JsonResponse({"message": "user authenticated"}, status=status.HTTP_200_OK)

    else:
        return JsonResponse({"message": "user not found"}, status=status.HTTP_401_UNAUTHORIZED)

