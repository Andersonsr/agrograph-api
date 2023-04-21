import os
from datetime import datetime

from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.db import IntegrityError
from ..model.writer import writeMeasurement
from app.model.models import UserProfile
from app.utils.constants import expirationTime
from neomodel.core import DoesNotExist
from dotenv import load_dotenv
load_dotenv()

cross_secret = os.environ.get('CROSS_SERVER_SECRET')


def checkLogin(email, token, secret):
    if email is not None:
        try:
            user = UserProfile.nodes.get(email=email)
            return user.uid
        except DoesNotExist:
            return False
    elif token is not None and secret is not None:
        try:
            user = UserProfile.nodes.get(lastToken=token)
            if (datetime.now() - user.lastLogin).total_seconds() < expirationTime and cross_secret == secret:
                return user.uid
        except DoesNotExist:
            return False
    return False
