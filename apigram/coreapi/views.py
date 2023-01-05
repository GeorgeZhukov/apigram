from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.




class CustomObtainAuthToken(ObtainAuthToken):
    """
    This endpoint returns token
    You should include this token with headers
    For example:
      Authorization: Token 03d2238e5408c076a8ff2735055ffbi471dcd0c1
    """
    
    pass