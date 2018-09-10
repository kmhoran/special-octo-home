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
                'completed_timestamp')

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ('id',
                  'user',
                  'display_name',
                  'date_created',
                  'is_complete')