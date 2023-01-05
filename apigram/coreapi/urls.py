from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import JSONOpenAPIRenderer

from .router import router



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token),
    # path('auth/', CustomAuthToken.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('redoc/', TemplateView.as_view(
        template_name='coreapi/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    path('openapi', get_schema_view(
        title="apigram",
        description="API for all apigram endpoints",
        version="1.0.0",
        urlconf='coreapi.urls',
        renderer_classes=[JSONOpenAPIRenderer]
    ), name='openapi-schema'),
]
