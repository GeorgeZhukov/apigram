from django.contrib.auth.models import User

from rest_framework import viewsets, response, generics
from rest_framework.viewsets import mixins
from rest_framework import permissions
from rest_framework.decorators import action

import logging


from .serializers import AccountSerializer, CreatePostSerializer, ListPostSerializer, PostPhotoSerializer, RegisterSerializer
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


# class AuthViewSet(viewsets.ModelViewSet):
#     """
#     This resource act as auth controller
#     """

#     queryset = User.objects.all()
#     serializer_class = AccountSerializer

    
#     @action(detail=False, methods=['post'])
#     def request_token(self, request):
#         """
#         Request a new token

#         Input: **username** and **password**

#         Output: **token**
#         """

#         return response.Response({'status': 'password set'})

#     @action(detail=False, methods=['post'])
#     def registrate(self, request):
#         """
#         Create a new user/account

#         Input: **username**, **password**, **password2**, **email**, **first_name**, **last_name**

#         Output: **id**, **username**, **email**, **first_name**, **last_name**
#         """

#         return response.Response({'status': 'registered'})


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

    Resource of all posts

    **Create post** -
    Before creating post resource you should create post photos and then use id of each saved record to create post

    For authorized users only
    """

    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        return super().get_serializer_class()
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user.account)



    



# class PostPhotoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
class PostPhotoViewSet(viewsets.ModelViewSet):
    """

    Resource of photos related to posts

    Create post photos before post itself and then use id of each saved record to create post

    For authorized users only

    """
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user.account)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    This endpoint to create a new user
    After new user created, you should request a new authenetication token

    """
    queryset = User.objects.none()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
