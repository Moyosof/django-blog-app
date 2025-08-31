from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name','bio',
                   'profile_picture', 'facebook', 'youtube', 'instagram', 'twitter']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        user = get_user_model()
        new_user = user.objects.create(email=email, username=username,
                                       first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return new_user
    

class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']

class BlogSerializer(serializers.ModelSerializer):
    author = SimpleAuthorSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'content', 'author', 'created_at', 'updated_at', 'published_date', 'is_draft', 'category', 'featured_image']
       # read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'published_date']