from django.test import TestCase
from django.utils import timezone
from lists.serializers import ListObjectSerializer, ListItemSerializer, ListItemCollectionSerializer
from homesiteusers.models import UserProfile
from django.contrib.auth.models import User
from lists.models import List
from rest_framework.exceptions import ValidationError


class ListItemSerializerMethods(TestCase):
    
    GOOD_PARENT_LIST = 1
    BAD_PARENT_LIST = 2

    def setUp(self):
        user = User.objects.create_user('first', 'some@email.com', 'pass')
        user.save()
        profile = UserProfile()
        profile.user = user
        profile.first_name = 'first'
        profile.save()

        parent_list_obj = List()
        parent_list_obj.display_name =  "the parent"
        parent_list_obj.profile = profile
        parent_list_obj.save()
        GOOD_PARENT_LIST = parent_list_obj.id

        

    def tearDown(self):
        pass

    
    def test_validateData_with_invalid_input_throws(self):
        with self.assertRaises(ValidationError):
            data = {}
            serializer = ListItemSerializer(data=data)
            
            serializer.is_valid(raise_exception=True)

    def test_validateData_minimum_valid_input_doesnt_throw(self):
        data = {
            'id': 0,
            'text': 'some text',
            'parent_list': self.GOOD_PARENT_LIST,
            'is_complete': False
        }
        serializer = ListItemSerializer(data=data)
        
        serializer.is_valid(raise_exception=True)

    
    
