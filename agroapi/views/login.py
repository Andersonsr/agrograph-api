from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from agroapi.model.models import UserProfile
from django.contrib.auth import authenticate


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return Response({'message': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    profile = UserProfile.nodes.get(email=email)
    if user is not None:
        request.session['email'] = email
        request.session['logged'] = 'yes'
        request.session['uid'] = profile.uid
        return Response({'message': 'user authenticated'}, status=status.HTTP_200_OK)

    else:
        return Response({'message': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)

