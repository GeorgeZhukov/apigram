from rest_framework import routers

from .viewsets import  RegisterViewSet, AccountViewSet, PostPhotoViewSet, PostViewSet, AccountPhotoViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'accounts', AccountViewSet)
router.register(r'account_photos', AccountPhotoViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'post_photos', PostPhotoViewSet)
router.register(r'posts', PostViewSet)

