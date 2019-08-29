from django.db import models
from django.conf import settings
from django.urls import reverse
from users.models import Group
import datetime

# Create your models here.
class ToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    due_date = models.DateField( blank=True, null=True)
    group = models.ForeignKey(Group, related_name='comments_associated_with_post', null=True, on_delete=models.CASCADE)
    is_in_progress = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    time_completed = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('to_do:to_do_create')
