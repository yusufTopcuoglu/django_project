from rest_framework import serializers

from scorp_app.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'full_name', 'profile_photo']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['owner', 'created_at', 'image_link']
