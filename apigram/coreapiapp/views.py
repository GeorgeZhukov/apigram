from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.
from .viewsets import CurrentVersioning

# TODO: remove/replace with viewset
class CustomObtainAuthToken(ObtainAuthToken):
    """

        This endpoint returns token in case if you send valid username and password

        **CURL Request example**:
        ```
        curl https://apigram.crabdance.com/api/v1/auth/ \\
            --data '{"username": "someusername", "password": "hardtorememberpassword"}' \\
            --header 'Content-Type: application/json'
        ```

        **Good response example**:
        ```
        {
            "token": "03d2238e5408c076a8ff2735055ffbi471dcd0c1"
        }
        ```

        **Bad response example**:
        ```
        {
            "type": "validation_error",
            "errors": [
                {
                    "code": "authorization",
                    "detail": "Unable to log in with provided credentials.",
                    "attr": "non_field_errors"
                }
            ]
        }
        ```

        You should include this token with headers

        Header name: **Authorization**

        Header value: **Token {{token}}**

        For example: **Authorization**: **Token 03d2238e5408c076a8ff2735055ffbi471dcd0c1**

        **CURL example:**
        ```
        curl https://apigram.crabdance.com/api/v1/accounts/ \\
            --header 'Content-Type: application/json' \\
            --header 'Authorization: Token 03d2238e5408c076a8ff2735055ffbi471dcd0c1'
        ```
    """
    # schema = AutoSchema(
    #     tags=['auth'],
    #     component_name='ObtainAuthToken',
    #     operation_id_base='ObtainAuthToken',
    # )
    versioning_class = CurrentVersioning
    def post(self, request, *args, **kwargs):
        print("my middleware {}".format(request.headers))
        return super().post(request, *args, **kwargs)
