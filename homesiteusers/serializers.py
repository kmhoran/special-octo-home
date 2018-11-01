from rest_framework import serializers
from homesiteusers.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields=('id',
                'user',
                'first_name')
        read_only_fields = ('id','user',)