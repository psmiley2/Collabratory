from django.db import models
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from users.models import Group
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Transpose, SmartResize

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    image_thumbnail = ImageSpecField(
        source='image',
        processors = [Transpose(),SmartResize(200, 200)],
        format = 'JPEG',
    )
    image_fullsize = ImageSpecField(
        source='image',
        processors = [Transpose()],
    )
    time_posted = models.DateTimeField(auto_now_add=True, blank=True)
    group = models.ForeignKey(Group, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '\'s post'

    def get_absolute_url(self):
        return reverse('forum:index')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments_associated_with_post',on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    time_posted = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.user) + '\'s Comment' + str(self.pk)

    def get_absolute_url(self):
        return reverse('forum:index')
