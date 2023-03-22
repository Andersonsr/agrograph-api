from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from django.contrib.auth.models import User
from agroapi.model.models import UserProfile


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def createUser(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        institution = request.POST['institution']
    except KeyError:
        return Response({'message': 'email, password, name, institution are required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=email)
    except User.DoesNotExist:
        try:
            User.objects.create_user(username=email, password=password)
            profile = UserProfile(institution=institution, name=name, email=email)
            profile.save()
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'message': 'this email is already registered'}, status=status.HTTP_403_FORBIDDEN)

    return Response({'message': 'this email is already registered'}, status=status.HTTP_403_FORBIDDEN)

