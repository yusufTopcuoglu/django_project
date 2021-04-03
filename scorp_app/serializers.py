from rest_framework import serializers

from scorp_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'full_name', 'profile_photo']
