from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from django.contrib.auth.models import User
from agroapi.models import UserProfile
from django.contrib.auth import authenticate


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def editUser(request):
    try:
        isLogged = 'logged' in request.session
        email = request.session['email']
        newName = request.POST['name']
        newEmail = request.POST['email']
        newPass = request.POST['password']
        newInst = request.POST['institution']
    except KeyError:
        return Response({'detail': 'you are not logged in'}, status=status.HTTP_403_FORBIDDEN)

    if isLogged:
        userProfile = UserProfile.nodes.get(email=email)
        user = User.objects.get(username=email)

        user.username = newEmail
        user.set_password(newPass)
        user.save()

        userProfile.institution = newInst
        userProfile.name = newName
        userProfile.email = newEmail
        userProfile.save()

        request.session['email'] = newEmail
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)

    return Response({'message': 'you are not logged in'}, status=status.HTTP_403_FORBIDDEN)


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def createUser(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        institution = request.POST['institution']
    except KeyError:
        return Response({'message': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=email)
    except User.DoesNotExist:
        try:
            User.objects.create_user(username=email, password=password)
            UserProfile(institution=institution, name=name, email=email).save()
            return Response({'message': 'ok'}, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'message': 'this email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'this email is already registered'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    try:
        email = request.GET['email']
        password = request.GET['password']
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
        return Response({'message': 'user not found'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def logout(request):
    try:
        del request.session['email']
        del request.session['logged']
        del request.session['id']
    except KeyError:
        pass
    return Response({'message': 'successfully logged off'}, status=status.HTTP_200_OK)

