from django.db import models
from django.utils import timezone
from homesiteusers.models import UserProfile

class List(models.Model):
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

    @property
    def completed_timestamp(self):
        return self.date_completed

    def set_date_complete(self, mark_done):
        if not mark_done:
            self.date_completed = None
        elif self.date_completed is None:
            self.date_completed = timezone.now()

    def __str__(self):
        return self.text