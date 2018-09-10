from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from homesiteusers.serializers import UserProfileSerializer
from homesiteusers.models import UserProfile

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)