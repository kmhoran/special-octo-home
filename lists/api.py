from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from lists.serializers import ListSerializer, ListItemSerializer
from lists.models import List, ListItem

class ListViewSet(ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def create(self, request):
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListItemViewSet(ModelViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer

    def create(self, request):
        serializer = ListItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)