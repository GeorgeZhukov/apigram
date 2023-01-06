from django.contrib.auth.models import User

from rest_framework import viewsets, response, generics
from rest_framework.viewsets import mixins
from rest_framework import permissions

import logging


from .serializers import AccountSerializer, PostSerializer, PostPhotoSerializer, RegisterSerializer
from .models import Account, Post, PostPhoto

logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        try:
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Instance must have an attribute named `owner`.
            return obj.owner == request.user
        except Exception as e:
            logger.warn("Exception while permission checking: {}".format(e))
            
            return False

# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """

    Returns a list of all **active** accounts in the system.

    For authorized users only
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    """

    Returns a list of all **active** posts

    For authorized users only
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    



# class PostPhotoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
class PostPhotoViewSet(viewsets.ModelViewSet):
    """

    Returns a list of photos related to posts

    For authorized users only

    """
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    This endpoint to create a new user
    After new user created, you should request a new authenetication token

    """
    queryset = User.objects.none()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
