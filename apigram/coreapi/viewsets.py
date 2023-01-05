from django.contrib.auth.models import User

from rest_framework import viewsets, response, generics
from rest_framework.viewsets import mixins
from rest_framework import permissions

from .serializers import AccountSerializer, PostSerializer, PostPhotoSerializer, RegisterSerializer
from .models import Account, Post, PostPhoto

# ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class AccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    **For authorized users**

    Returns a list of all **active** accounts in the system.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """
    **For authorized users**

    Returns a list of all **active** posts
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    



# class PostPhotoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
class PostPhotoViewSet(viewsets.ModelViewSet):
    """
    **For authorized users**

    Returns a list of photos related to posts
    """
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    This endpoint to create a new user
    After new user created, you should request a new authenetication token
    """
    queryset = User.objects.none()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
