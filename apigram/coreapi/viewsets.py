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
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all **active** posts

    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]



    # def retrieve(self, request, *args, **kwargs):
    #     print("kwargs: {}".format(kwargs))
    #     queryset = Post.objects.filter(pk=kwargs['pk']).first()
    #     # return super().retrieve(request, *args, **kwargs)
    #     serializer = PostSerializer(queryset, context={'request': request})

        
    #     return response.Response(data=serializer.data)



class PostPhotoViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    Returns a list of photos related to **specific** post
    """
    queryset = PostPhoto.objects.all()
    serializer_class = PostPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def retrieve(self, request, *args, **kwargs):
    #     print("kwargs: {}".format(kwargs))
    #     queryset = PostPhoto.objects.filter(post_id=kwargs['post_pk'], pk=kwargs['pk']).first()
    #     serializer = PostPhotoSerializer(queryset, context={'request': request})

    #     return response.Response(data=serializer.data)

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if 'post_pk' in self.kwargs:
    #       queryset = queryset.filter(post_id=self.kwargs['post_pk'])
        
    #     print("queryset: {} {}".format(queryset, self.kwargs))
    #     return queryset


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.none()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
