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
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView, TemplateView

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.schemas import get_schema_view
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='api/schema/swagger-ui/', permanent=False)),
    # path('api/v1/', include('coreapiapp.urls')),
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='openapi-schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='openapi-schema'), name='redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^api/v1/', include('coreapiapp.urls', namespace='v1')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('swifty_panel/', admin.site.urls),
    # path('openapi', get_schema_view(
    #     title="Your Project",
    #     description="API for all things …",
    #     version="v1",
    #     urlconf='coreapiapp.urls',
        
    #     # patterns=schema_url_patterns,
    # ), name='openapi-schema'),
    path('openapi', get_schema_view(

        title="APIGRAM",

        # description="API for all things …",
        version="v1",

        urlconf='coreapiapp.urls',
        url='/api/v1',
        public=True,
        authentication_classes=[SessionAuthentication, TokenAuthentication],
        
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='coreapi/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]


if settings.DEBUG:
    urlpatterns = [
        *urlpatterns,
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




