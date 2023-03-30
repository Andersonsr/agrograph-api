from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth.models import User
from app.model.models import UserProfile


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def editUser(request):
    try:
        isLogged = 'logged' in request.session
        email = request.session['email']
    except KeyError:
        return JsonResponse({'message': 'you are not logged in'}, status=status.HTTP_403_FORBIDDEN)

    try:
        newName = request.POST['name']
        newEmail = request.POST['email']
        newPass = request.POST['password']
        newInst = request.POST['institution']
    except KeyError:
        return JsonResponse({'message': 'name, email, password, institution are required'},
                            status=status.HTTP_400_BAD_REQUEST)

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
        return JsonResponse({'message': 'ok'}, status=status.HTTP_200_OK)

    return JsonResponse({'message': 'you are not logged in'}, status=status.HTTP_403_FORBIDDEN)
