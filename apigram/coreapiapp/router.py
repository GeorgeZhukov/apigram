from rest_framework import routers

from .viewsets import  AccountViewSet, PostViewSet, PostPhotoViewSet, RegisterViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()


# router.register(r'users', UserViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'posts', PostViewSet)
router.register(r'post_photos', PostPhotoViewSet)
