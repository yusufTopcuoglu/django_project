from rest_framework import serializers

from scorp_app.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'full_name', 'profile_photo']


class PostSerializer(serializers.ModelSerializer):
    # this maybe a HyperlinkedRelatedField to navigate users profile on click
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = ['owner', 'created_at', 'image_link']
        depth = 1
