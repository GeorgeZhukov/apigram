"""apigram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView


# from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from rest_framework.renderers import JSONOpenAPIRenderer

# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# schema_view = get_schema_view(
#     title="apigram",
#     description="API for all apigram endpoints",
#     version="1.0.0",
#     # urlconf='urls',
#     renderer_classes=[JSONOpenAPIRenderer]
# )
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Apigram API",
#       default_version='v1',
#       description="Apigram API",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="scofield.cross@gmail.com"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
#    authentication_classes=[SessionAuthentication, TokenAuthentication]
# )

urlpatterns = [
    path('', RedirectView.as_view(url='api/schema/swagger-ui/', permanent=False)),
    path('api/v1/', include('coreapiapp.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('admin/', admin.site.urls),
    
    # path('redoc/', TemplateView.as_view(
    #     template_name='coreapi/redoc.html',
    #     extra_context={'schema_url':'openapi-schema'}
    # ), name='redoc'),
    # path('openapi', schema_view, name='openapi-schema'),
    # path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG or True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




