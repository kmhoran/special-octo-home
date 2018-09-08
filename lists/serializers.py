from rest_framework import serializers
from lists.models import List, ListItem

class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields=('id',
                'parent_list',
                'text',
                'ordinal',
                'is_complete',
                'date_created',
                'date_completed')

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id',
                  'user',
                  'display_name',
                  'date_created',
                  'listitem_set',
                  'is_complete')