from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.http import JsonResponse


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def logout(request):
    try:
        del request.session['email']
        del request.session['logged']
        del request.session['id']
    except KeyError:
        pass
    return JsonResponse({"message": "successfully logged off"}, status=status.HTTP_200_OK)

