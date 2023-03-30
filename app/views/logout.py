from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse
from app.model.models import UserProfile
from django.contrib.auth import authenticate


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def login(request):
    try:
        email = request.POST['email']
        password = request.POST['password']
    except KeyError:
        return JsonResponse({'message': 'something is wrong with your request'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)
    profile = UserProfile.nodes.get(email=email)
    if user is not None:
        request.session['email'] = email
        request.session['logged'] = 'yes'
        request.session['uid'] = profile.uid
        return JsonResponse({'message': 'user authenticated'}, status=status.HTTP_200_OK)

    else:
        return JsonResponse({'message': 'user not found'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def logout(request):
    try:
        del request.session['email']
        del request.session['logged']
        del request.session['id']
    except KeyError:
        pass
    return JsonResponse({'message': 'successfully logged off'}, status=status.HTTP_200_OK)

