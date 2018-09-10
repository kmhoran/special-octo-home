from rest_framework import serializers
from homesiteusers.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=('user',
                'first_name')