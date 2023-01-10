from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account, Post, PostPhoto, AccountPhoto


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'is_active', 'date_joined']


class AccountPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, write_only=False)

    class Meta:
        model = AccountPhoto
        read_only_fields = ['id', 'account', 'created_at']
        fields = ['photo']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    account_photo = serializers.ImageField(source='account_photo.photo')

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_photo', 'created_at', 'updated_at']


class PostPhotoSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField(use_url=True, write_only=False)

    class Meta:
        model = PostPhoto
        fields = ['id', 'photo']


class AuthorFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(AuthorFilteredPrimaryKeyRelatedField,
                         self).get_queryset()
        if not request or not queryset:
            return queryset.none()
        return queryset.filter(author=request.user.account)


class PostSerializer(serializers.ModelSerializer):
    post_photos = AuthorFilteredPrimaryKeyRelatedField(
        many=True, queryset=PostPhoto.objects.filter(post=None,), write_only=True)
    photos = PostPhotoSerializer(
        many=True, read_only=True, source='post_photos')

    def validate_post_photos(self, post_photos: list[PostPhoto]):
        account = self.context['request'].user.account
        pk_list = map(lambda item: item.pk, post_photos)
        queryset = account.postphoto_set.filter(pk__in=pk_list, post=None)
        if not queryset.exists():
            raise serializers.ValidationError(
                detail='No photos to add to post')
        return queryset

    def create(self, validated_data):
        account = self.context['request'].user.account

        post = Post.objects.create(
            author=account,
            description=validated_data['description']
        )

        pk_list = map(lambda item: item.pk, validated_data['post_photos'])
        _updated = account.postphoto_set.filter(
            pk__in=pk_list).update(post=post)

        return post

    class Meta:
        model = Post
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        fields = ['id', 'author', 'description', 'post_photos',
                  'photos', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs
