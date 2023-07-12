import json
import os
from datetime import datetime
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from ..model.writer import writeMeasurement
from app.model.models import UserProfile
from app.utils.constants import EXPIRATION_TIME
from neomodel.core import DoesNotExist
from dotenv import load_dotenv
import jwt


def checkLogin(request):
    load_dotenv()
    cross_secret = os.environ.get('CROSS_SERVER_SECRET')

    # session authentication
    email = request.session.get('email')
    if email is not None:
        try:
            user = UserProfile.nodes.get(email=email)
            return user.uid, None
        except DoesNotExist:
            return False, None

    # token cross server authentication
    if request.method == "POST":
        if 'jwt' not in request.POST:
            return False, None

        print("received "+str(request.POST['jwt']))
        data = jwt.decode(request.POST['jwt'], cross_secret, algorithms=["HS256"])

    elif request.method == "GET":
        if 'jwt' not in request.GET:
            return False, None
        data = jwt.decode(request.GET['jwt'], cross_secret, algorithms=["HS256"])

    # check token expiration time
    if data is not None:
        try:
            user = UserProfile.nodes.get(lastToken=data['authToken'])
            if (datetime.now() - user.lastLogin).total_seconds() < EXPIRATION_TIME:
                return user.uid, data

        except DoesNotExist:
            return False, None
        except AttributeError:
            return False, None
    return False
