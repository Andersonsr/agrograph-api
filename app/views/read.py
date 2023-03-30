import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from ..model.reader import readMeasurementsQuery, readUserMeasurements
from ..utils.filters import applyALlFilters


@api_view(('GET', ))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def read(request):
    try:
        email = request.session['email']
        uid = request.session['uid']
        logged = request.session['logged'] == 'yes'
    except AttributeError:
        return Response({'message': 'not authorized, login first'}, status=status.HTTP_403_FORBIDDEN)

    if logged:
        dateMin = request.GET.get("date-min")
        dateMax = request.GET.get("date-max")
        polygon = request.GET.get("polygon")
        valueMax = request.GET.get("value-max")
        valueMin = request.GET.get("value-min")
        timeMin = request.GET.get("time-min")
        timeMax = request.GET.get("time-max")
        varName = request.GET.get("name")
        category = request.GET.get("category")

        try:
            data = applyALlFilters(email, uid, polygon, dateMin, dateMax, valueMin, valueMax, timeMin, timeMax, varName,
                                   category)
        except KeyError:
            return Response({'message': 'User has no measurements'}, status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'message': 'value-max and value-min must be float'}, status.HTTP_400_BAD_REQUEST)
        return Response(json.dumps(data), status=status.HTTP_200_OK)
    return
