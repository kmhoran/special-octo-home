from django.utils import timezone
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework import viewsets
from library.exceptions.restExceptions import ApplicationException, ArgumentException, NotAllowedException
from lists.serializers import ListObjectSerializer, ListItemSerializer
from lists.models import List, ListItem


DEFAULT_USER_ID = 1

class ListsViewSetApi(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = List.objects.filter(user = DEFAULT_USER_ID)
    serializer_class = ListObjectSerializer
    base_name = 'list'

    def perform_create(self, serializer):
        serializer.save()

    def filter_queryset(self, full_set):
        return full_set.filter(user = DEFAULT_USER_ID)


class ListsItemViewSetApi(viewsets.GenericViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer
    base_name = 'item-collection'

    def filter_queryset(self, full_set, parent_list):
        return full_set.filter(parent_list = parent_list)
    
    def sort_items(self, items):
        return sorted(items, key = lambda i : i.get('ordinal'))

    # collection actions
    @action(methods=['get','post', 'put'],
        detail=False,
        url_name='items',
        url_path='(?P<parent_list>[0-9]+)/items')
    def CreateAndRetrieveListItemsApi(self, request, parent_list=None):
        """
        => .../{parent_list}/items/
        Create and List items for a designated list
        """
        if parent_list is None:
            raise ArgumentException("No parent list provided.")
        
        # create
        if request.method == 'POST':
            return self.create_instance(request, parent_list)

        # get collection
        elif request.method == 'GET':
            return self.get_collection(request, parent_list)

        # update collection
        elif request.method == 'PUT':
            return self.update_collection(request, parent_list)
        else:

            # we should never get to this point
            raise NotAllowedException("Method {method} not allowed.".format(method=request.method))

    def create_instance(self, request, parent, *args, **kwargs):
        print('creating!')
        req_parent = request.data.get('parent_list')
        if int(parent) != int(req_parent):
            print('api | collections | parent: {parent}, req: {req}'.format(parent=parent, req=req_parent))
            raise ArgumentException("Requested parents do not match.")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_collection(self, request, parent, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), parent)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.sort_items(serializer.data))

    def update_collection(self, request, parent, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(), parent)

        # not sure now to load insatnces into serializer...
        serializer = self.get_serializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(self.sort_items(serializer.data))

    # instance actions
    @action(methods=['get','put'],

            # detail=True adds undesireable functionality to the routing
            detail=False,
            url_name='item-detail',
            url_path='(?P<parent_list>[0-9]+)/items/(?P<item_id>[0-9]+)')
    def UpdateListItemApi(self, request, parent_list=None, item_id=None):
        """
        => .../{pk}/items/{item_id}/
        Updates single item for a designated list
        """
        if parent_list is None:
            raise ArgumentException("No parent list provided.")
        
        # validate entity exists
        try:
            exististing_instance = self.get_queryset().get(id = item_id, parent_list=parent_list)
        except:
            raise ArgumentException("Item {pk} does not belong to list {parent}".format(pk=item_id, parent=parent_list))
        
        if request.method == 'PUT':

            # update instance
            serializer = self.get_serializer(exististing_instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # get instance
        elif request.method == 'GET':
            serializer = self.get_serializer(exististing_instance)
            return Response(serializer.data)
        else:

            # we should never get to this point
            raise NotAllowedException("Method {method} not allowed.".format(method=request.method))


        

