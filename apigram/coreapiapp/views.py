from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.


# TODO: remove/replace with viewset
class CustomObtainAuthToken(ObtainAuthToken):
    """
    This endpoint returns token
    You should include this token with headers
    
    Header name: **Authorization**

    Header value: **Token {{token}}**

    For example: **Authorization**: **Token 03d2238e5408c076a8ff2735055ffbi471dcd0c1**
    """
    # schema = AutoSchema(
    #     tags=['auth'],
    #     component_name='ObtainAuthToken',
    #     operation_id_base='ObtainAuthToken',
    # )
    def post(self, request, *args, **kwargs):
        print("my middleware {}".format(request.headers))
        return super().post(request, *args, **kwargs)