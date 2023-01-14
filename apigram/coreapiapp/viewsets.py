from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, filters
from rest_framework.viewsets import mixins
from rest_framework.decorators import action
from rest_framework.versioning import NamespaceVersioning

from django_filters.rest_framework import DjangoFilterBackend

import logging


from .serializers import AccountSerializer, PostSerializer, PostPhotoSerializer, RegisterSerializer, AccountPhotoSerializer
from .models import Account, Post, PostPhoto, AccountPhoto

logger = logging.getLogger(__name__)


class CurrentVersioning(NamespaceVersioning):
    default_version = 'v1'
    allowed_versions = ['v1']


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


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
        # Accounts

        Returns a list of all **active** accounts in the system.

        ## Notes
        It also includes:

        1. link to related **account photo** record
        1. account photo url (thumbnail version)

        For authorized users only

    """
    # schema = AutoSchema(
    #     tags=['Account'],
    #     component_name='Account',
    #     operation_id_base='Account',
    # )
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]
    versioning_class = CurrentVersioning

    def get_queryset(self):

        return super().get_queryset()


class AccountPhotoViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """
        Resource of account photos

        Contains two version of photos, **medium** and **small** for effectively renders list of records

        **Note**:

        1. **UPDATE** (PUT, PATCH) actions allowed only for **owners**
        1. **medium** - means resoultion of photo approximately 512px x 512px
        1. **small** or **thumbnail** - approximately 128px x 128px

        For authorized users only
    """
    # schema = AutoSchema(
    #     tags=['AccountPhoto'],
    #     component_name='AccountPhoto',
    #     operation_id_base='AccountPhoto',
    # )
    queryset = AccountPhoto.objects.all()
    serializer_class = AccountPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    versioning_class = CurrentVersioning

    def get_queryset(self):
        return super().get_queryset()


class PostViewSet(viewsets.ModelViewSet):
    """
        Resource of all posts

        **Create post** -
        Before creating post resource you should create [post photos][ref] and then use id of each saved record to create post

        For authorized users only

        [ref]: /api/v1/post_photos/
    """
    # schema = AutoSchema(
    #     tags=['Post'],
    #     component_name='Post',
    #     operation_id_base='Post',
    # )
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['author__user__username', ]
    versioning_class = CurrentVersioning

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user.account)


# class PostPhotoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
class PostPhotoViewSet(viewsets.ModelViewSet):
    """
        Resource of photos related to posts

        Create post photos before post itself and then use id of each saved record to create [post][ref]

        For authorized users only

        [ref]: /api/v1/posts/
    """
    # schema = AutoSchema(
    #     tags=['PostPhoto'],
    #     component_name='PostPhoto',
    #     operation_id_base='PostPhoto',
    # )
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['=post__id']
    versioning_class = CurrentVersioning

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user.account)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
        This endpoint to create a new user
        After new user created, you should request a new authenetication token [see here][ref]
        # Tutorial (displayed in the left navigation)
        # Errors

        We follow the error response format proposed in [RFC 7807](https://tools.ietf.org/html/rfc7807)
        also known as Problem Details for HTTP APIs. As with our normal API responses,
        your client must be prepared to gracefully handle additional members of the response.

        ## Unauthorized

            <RedocResponse pointer={"#/components/responses/Unauthorized"} />

        ## AccessForbidden

            <RedocResponse pointer={"#/components/responses/AccessForbidden"} />

        [ref]: ./v1_auth_create
    """
    # schema = AutoSchema(
    #     tags=['auth'],
    #     component_name='Registration',
    #     operation_id_base='Register',
    # )
    queryset = User.objects.none()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    versioning_class = CurrentVersioning

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])

        return user.save()
