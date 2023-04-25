from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth.models import User
from app.model.models import UserProfile
from app.utils.checkLogin import checkLogin
from neomodel.core import DoesNotExist


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def editUser(request):
    uid = checkLogin(request)
    if not uid:
        return JsonResponse({'message': 'not authorized, login first'}, status=status.HTTP_401_UNAUTHORIZED)

    newName = request.POST['name']
    newEmail = request.POST['email']
    newPass = request.POST['password']
    newInst = request.POST['institution']

    try:
        userProfile = UserProfile.nodes.get(uid=uid)
        user = User.objects.get(username=userProfile.email)
    except User.DoesNotExist:
        JsonResponse({'message': 'user do not exist'}, status=status.HTTP_400_BAD_REQUEST)

    except DoesNotExist:
        JsonResponse({'message': 'user do not exist'}, status=status.HTTP_400_BAD_REQUEST)

    user.username = newEmail
    user.set_password(newPass)
    user.save()

    userProfile.institution = newInst
    userProfile.name = newName
    userProfile.email = newEmail
    userProfile.save()

    request.session['email'] = newEmail
    return JsonResponse({"message": "ok"}, status=status.HTTP_200_OK)

