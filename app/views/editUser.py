from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth.models import User
from app.model.models import UserProfile
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def editUser(request):
    """
    API endpoint for editing user information.

    Method: POST

    Parameters:
    - newName: The new name for the user (required)
    - newEmail: The new email for the user (required)
    - newPassword: The new password for the user (required)
    - newInstitution: The new institution for the user (required)

    Returns:
    - 200 OK: User information updated successfully
    - 400 BAD REQUEST: Missing or invalid parameters
    - 401 UNAUTHORIZED: User authentication failed
    - 500 INTERNAL SERVER ERROR: An error occurred while updating user information
    """
    data = request.POST

    newName = data.get('newName')
    newEmail = data.get('newEmail')
    newPass = data.get('newPassword')
    newInst = data.get('newInstitution')

    if not all([newName, newEmail, newPass, newInst]):
        return JsonResponse({'message': 'Missing or invalid parameters.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = request.user
        userProfile = UserProfile.nodes.first_or_none(email=user.username)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    if userProfile is None:
        return JsonResponse({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the new email is already taken by another user
    existing_user_profile = UserProfile.nodes.first_or_none(email=newEmail)
    if existing_user_profile is not None and existing_user_profile != userProfile:
        return JsonResponse({'message': 'Email is already taken by another user.'}, status=status.HTTP_403_FORBIDDEN)

    user.username = newEmail
    user.set_password(newPass)
    user.save()

    userProfile.name = newName
    userProfile.email = newEmail
    userProfile.institution = newInst
    userProfile.save()

    request.session['email'] = newEmail
    return JsonResponse({"message": "User information updated successfully."}, status=status.HTTP_200_OK)
