from django.urls import path, include

from rest_framework.authtoken import views

from .router import router



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token),
    # path('auth/', CustomAuthToken.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
