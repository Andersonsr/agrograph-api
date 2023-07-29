from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@authentication_classes([SessionAuthentication, TokenAuthentication])
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'User authentication failed, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    logout(request)
    return JsonResponse({"message": "successfully logged off"}, status=status.HTTP_200_OK)

