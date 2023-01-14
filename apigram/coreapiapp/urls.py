from django.urls import path, include
from rest_framework.schemas import get_schema_view


from .router import router
from .views import CustomObtainAuthToken

app_name = 'coreapiapp'

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomObtainAuthToken.as_view()),
    # path('auth/', CustomAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
