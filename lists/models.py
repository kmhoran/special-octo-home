from django.db import models
from django.db.models import Max
from django.utils import timezone
from homesiteusers.models import UserProfile
from library.errorLog import get_logger
logger = get_logger(__name__)

class List(models.Model):
    def construct(self, user, **kwargs):
        logger.info('constructing List "{}"'.format(kwargs.get('display_name')))
        self.user = user
        self.display_name = kwargs.get('display_name')

    user = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE,)
    display_name = models.CharField(
        max_length=250, 
        default=None,)
    date_created = models.DateTimeField(
        default = timezone.now,
        editable=False,
        blank=True,)

    @property
    def is_complete(self):
        if self.id is None:
            return False
        items = ListItem.objects.filter(parent_list=self.id)
        if len(items) == 0:
            return False
        for item in items:
            if not item.is_complete:
                return False
        return True
    
    def __str__(self):
        return "{id}. {name}".format(
            id=self.id, 
            name=self.display_name)
        



class ListItem(models.Model):
    def construct(self,*args, **kwargs):
        logger.info('constructing ListItem {} for List {}'.format(kwargs.get('text'), kwargs.get('parent_list')))
        self.parent_list = kwargs.get('parent_list')
        self.text = kwargs.get('text')
        self.ordinal = self.determine_ordinal(kwargs.get('ordinal'))
        completed = kwargs.get('is_complete', False)
        self.is_complete = completed
        self.set_date_complete(completed)
        self.ordinal = self.determine_ordinal(kwargs.get('ordinal'))
        print("[models] initial ordinal is {ord}".format(ord=self.ordinal))


    parent_list = models.ForeignKey(
        List, 
        on_delete=models.CASCADE,)
    text = models.CharField(
        max_length=1000,
        null=False,
        blank=False,)
    ordinal = models.IntegerField()
    is_complete = models.BooleanField(
        default=False,
        null=False,)
    date_created = models.DateTimeField(
        default = timezone.now,
        editable=False,
        blank=True,)
    date_completed = models.DateTimeField(
        null=True,
        default=None,)


    def set_date_complete(self, mark_done):
        if not mark_done:
            logger.info('set List Item {} complete date to None'.format(self.id))
            self.date_completed = None
        elif self.date_completed is None:
            logger.info('set List Item {} complete date to {}'.format(timezone.now()))
            self.date_completed = timezone.now()
    def determine_ordinal(self, passed_ord):
        if passed_ord is not None:
            existing_instance = ListItem.objects.filter(parent_list = self.parent_list).filter(ordinal = passed_ord)
            if existing_instance is None:
                logger.info('returning original item instance ordinal {}'.format(passed_ord))
                return passed_ord
            
        max_aggregate = ListItem.objects.filter(parent_list = self.parent_list).aggregate(Max('ordinal'))
        current_highest = max_aggregate.get('ordinal__max')
        if current_highest is not None:
            logger.info('returning calculated item instance ordinal {}'.format(current_highest + 1))
            return current_highest + 1
        else:
            logger.warning('returning fall-through value ordinal 0. Something is wrong.')
            return 0

    def __str__(self):
        return self.text