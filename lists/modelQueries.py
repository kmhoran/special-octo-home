# from abc import ABC, abstractmethod
# from django.db import models
# from lists.models import List, ListItem
# from library.exceptions.restExceptions import ArgumentException, ApplicationException
# from library.errorLog import get_logger, log_error
# logr = get_logger(__name__)

# class QueryBase(ABC):
#     def __init__(self, entity):
#         if entity is None:
#             ex = log_error(logr,ArgumentException("Entity must be set for model query"))
#             raise ex
#         self._entity = entity
    
#     @abstractmethod
#     def get_all(self):
#         ex = NotImplementedError("get_all not implemented")
#         logger.exception(ex)
#         raise ex

#     @property
#     def entity(self):
#         if self._entity is None:
#             ex = ApplicationException("Entity not set for model query")
#             logger.exception(ex)
#             raise ex

# class ListItemQueries(QueryBase):
#     def get_all(self):
#         return self.entity.objects.all()