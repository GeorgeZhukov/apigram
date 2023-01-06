from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account, Post, PostPhoto



# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['email', 'username', 'is_active', 'date_joined']


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'user', 'created_at', 'updated_at' ]


class PostPhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostPhoto
        fields = [ 'id', 'post',  'photo' ]

    def create(self, validated_data):
        queryset = Post.objects.filter(author=self.context['request'].user.account)
        if 'post' in validated_data and validated_data['post']:
            if not queryset.filter(pk=validated_data['post'].pk).exists():
                raise serializers.ValidationError("You can't add photos to other users posts")

        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    post_photos = PostPhotoSerializer(many=True, read_only=True)
    

    class Meta:
        model = Post
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
        fields = [ 'id', 'author', 'description', 'post_photos','created_at', 'updated_at' ]

    def create(self, validated_data):
        account = self.context['request'].user.account

        post = Post.objects.create(
            author=account,
            description=validated_data['description']
        )
        return post



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user