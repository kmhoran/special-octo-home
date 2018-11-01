# from django.db import models
# from django.db.models import Max
# from lists.models import List, ListItem
# from library.exceptions.restExceptions import ArgumentException, ApplicationException
# from library.errorLog import get_logger, log_app_errors
# logger = get_logger(__name__)


# class ListItemService:

#     def _determine_ordinal(self, passed_ord, parent_list):
#         logger.warning("determine ordinal should really go in the queries module")
#         if passed_ord is not None:
#             existing_instance = ListItem.objects.filter(parent_list = parent_list).filter(ordinal = passed_ord)
#             if existing_instance is None:
#                 logger.info('returning original item instance ordinal {}'.format(passed_ord))
#                 return passed_ord
#         max_aggregate = ListItem.objects.filter(parent_list = parent_list).aggregate(Max('ordinal'))
#         current_highest = max_aggregate.get('ordinal__max')
#         if current_highest is not None:
#             logger.info('returning calculated item instance ordinal {}'.format(current_highest + 1))
#             return current_highest + 1
#         else:
#             logger.warning('returning fall-through value ordinal 0. Something is wrong.')
#             return 0

#     def _create_instance(self, *args, **kwargs):
#         logger.info('creating ListItem instance: {}'.format(str(kwargs).replace(',','..')))
#         parent = kwargs.get('parent_list')
#         text = kwargs.get('text')
#         logger.info('constructing ListItem {} for List {}'.format(text, parent))

#         newListItem = ListItem()
#         newListItem.parent_list = parent
#         newListItem.text = text
#         passed_ordinal = kwargs.get('ordinal')
#         newListItem.ordinal = self._determine_ordinal(passed_ordinal, parent)
#         completed = kwargs.get('is_complete', False)
#         newListItem.is_complete = completed
#         newListItem.set_date_complete(completed)
#         print("create instance: {}".format(newListItem.text))
#         return newListItem

#     def create_instance(self, *args, **kwargs):
#         print(kwargs)
#         new_instance = self._create_instance(*args, **kwargs)
#         print("instance: {}".format(new_instance.text))
#         # new_instance.save()
#         return new_instance

#     def _validate_input(self, data, instances, size):
#         instance_ids = [i.id for i in instances]
#         seen_ids = []
#         seen_ordinals = []
#         for d in data:
#             pk = d.get('id')
#             ordi = d.get('ordinal')
#             if pk is None:
#                 raise ArgumentException('Item id could not be found')
#             if ordi is None:
#                 raise ArgumentException('Item {pk} requires a valid ordinal value'.format(pk=pk))
#             if pk not in instance_ids:
#                 raise ArgumentException('Item {pk} is not part of the current collection'.format(pk=pk))
#             if ordi >= size:
#                 raise ArgumentException('ordinal value {ordi} is beyond the range of this collection: {s}'.format(ordi=ordi, s=size-1))
#             if pk in seen_ids:
#                 raise ArgumentException('Duplicate Item {pk} found. Cannot update'.format(pk=pk))
#             if ordi in seen_ordinals:
#                 raise ArgumentException('Cannot set multiple items to ordinal {ordi}'.format(ordi=ordi))
#             seen_ids.append(pk)
#             seen_ordinals.append(ordi)
            
#     def _get_ordinal(self, old_ord, taken_ords, size):
#         counter = size
#         try_ord = old_ord % size
#         while counter > 0:
#             if try_ord not in taken_ords:
#                 return try_ord
#             try_ord = (try_ord + 1) % size
#             counter = counter - 1
#         raise ApplicationException("Out of collection range")

#     def _set_collection_ordinals(self, instance_set, data):
         
#         instances = sorted(instance_set, key = lambda i : i.ordinal)
#         collection_size = count=len(instances)
#         self._validate_input(data, instances, collection_size)
#         data_ids = [d.get('id') for d in data]
#         data_intances = {i.id: i for i in instances if i.id in data_ids}
#         taken_ords = []
#         return_array = []

#         # explicitly set user-defined ordinals
#         for d in data:
#             inst = data_intances.get(d.get('id'))
#             if inst is None:
#                 raise ApplicationException('Item instance could not be found')
#             inst.ordinal = d.get('ordinal')
#             return_array.append(inst)
#             taken_ords.append(inst.ordinal)
        
#         # implicitly determine remaining ordinals
#         for i in instances:
#             if i.id in data_ids:
#                 continue
#             original_ord = i.ordinal
#             i.ordinal = self._get_ordinal(i.ordinal, taken_ords, collection_size)
#             #if i.ordinal != original_ord:
#             return_array.append(i)
#             taken_ords.append(i.ordinal)

#         return return_array

#     def set_collection_ordinals(self, instance_set, data):
#         updated_array = self._set_collection_ordinals(instance_set, data)
#         updated_array.sort(key = lambda i : i.ordinal)

#         # refractor to only update on ordinal change
#         logger.warn("currently updating data that has not changed!")
#         for inst in updated_array:
#             inst.save()
#         return updated_array