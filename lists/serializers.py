from rest_framework import serializers
from lists.models import List, ListItem
from homesiteusers.serializers import UserProfileSerializer
from library.exceptions.restExceptions import ArgumentException, ApplicationException
from library.errorLog import get_logger, log_app_errors
logger = get_logger(__name__)

class ListReferenceSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)

class ListItemCollectionSerializer(serializers.ListSerializer):
    def validate_input(self, data, instances, size):
        instance_ids = [i.id for i in instances]
        seen_ids = []
        seen_ordinals = []
        for d in data:
            pk = d.get('id')
            ordi = d.get('ordinal')
            if pk is None:
                raise ArgumentException('Item id could not be found')
            if ordi is None:
                raise ArgumentException('Item {pk} requires a valid ordinal value'.format(pk=pk))
            if pk not in instance_ids:
                raise ArgumentException('Item {pk} is not part of the current collection'.format(pk=pk))
            if ordi >= size:
                raise ArgumentException('ordinal value {ordi} is beyond the range of this collection: {s}'.format(ordi=ordi, s=size-1))
            if pk in seen_ids:
                raise ArgumentException('Duplicate Item {pk} found. Cannot update'.format(pk=pk))
            if ordi in seen_ordinals:
                raise ArgumentException('Cannot set multiple items to ordinal {ordi}'.format(ordi=ordi))
            seen_ids.append(pk)
            seen_ordinals.append(ordi)
            
    def get_ordinal(self, old_ord, taken_ords, size):
        counter = size
        try_ord = old_ord % size
        while counter > 0:
            if try_ord not in taken_ords:
                return try_ord
            try_ord = (try_ord + 1) % size
            counter = counter - 1
        raise ApplicationException("Out of collection range")

    # log_app_errors will log any exceptions caught along with the stack trace
    @log_app_errors
    def update(self, instance_set, data):
        """
        update ordinals in a collection of ListItems
        """
        instances = sorted(instance_set, key = lambda i : i.ordinal)
        collection_size = count=len(instances)
        self.validate_input(data, instances, collection_size)
        data_ids = [d.get('id') for d in data]
        data_intances = {i.id: i for i in instances if i.id in data_ids}
        taken_ords = []

        # explicitly set user-defined ordinals
        for d in data:
            inst = data_intances.get(d.get('id'))
            if inst is None:
                raise ApplicationException('Item instance could not be found')
            inst.ordinal = d.get('ordinal')
            inst.save()
            taken_ords.append(inst.ordinal)
        
        # implicitly determine remaining ordinals
        for i in instances:
            if i.id in data_ids:
                continue
            original_ord = i.ordinal
            i.ordinal = self.get_ordinal(i.ordinal, taken_ords, collection_size)
            if i.ordinal != original_ord:
                i.save()
            taken_ords.append(i.ordinal)
            
        return instances

class ListItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(max_length=1000)
    parent_list = serializers.PrimaryKeyRelatedField(queryset=List.objects.all())
    ordinal = serializers.IntegerField(required=False)
    is_complete = serializers.BooleanField()
    date_completed = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        instance create
        """
        newListItem = ListItem()
        newListItem.construct(**validated_data)
        newListItem.save()
        return newListItem
    
    def update(self, instance, validated_data):
        """
        instance update to alter 'text' & 'is_complete' fields
        """
        instance.text = validated_data.get('text',instance.text)
        completed = validated_data.get('is_complete', instance.is_complete)
        instance.is_complete = completed
        instance.set_date_complete(completed)
        instance.save()
        return instance
    
    class Meta:
        list_serializer_class = ListItemCollectionSerializer


class ListObjectSerializer(serializers.Serializer):
        
        id = serializers.IntegerField(read_only=True)
        user = UserProfileSerializer(read_only=True)
        display_name = serializers.CharField(max_length=250)
        date_created = serializers.DateTimeField(read_only=True)
        is_complete = serializers.BooleanField(read_only=True)
        
        def create(self, validated_data):
            if validated_data.get('user') is not None:
                ex = ArgumentException('user argument should not be set')
                logger.exception(ex)
                raise ex
            user = 1
            logger.warning('user hardcoded to 1')
            newList = List()
            newList.construct(user=user, **validated_data)
            newList.save()
            return newList
        
        def update(self, instance, validated_data):
            instance.display_name = validated_data.get('display_name', instance.display_name)
            instance.save()
            return instance
