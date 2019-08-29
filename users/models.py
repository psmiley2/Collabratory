from django.db import models
from django.conf import settings


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=100)
    max_group_size = models.IntegerField()
    total_students = models.IntegerField()
    current_project_student_count = models.IntegerField(default=0)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    project_code = models.CharField(max_length=15, default='')
    directions = models.TextField(default='')
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class Group(models.Model):
    title = models.CharField(max_length=100, blank=False, default='default_title', null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1, null=True, related_name='projects_associated_with_group') #should be labeled groups assosiated with projects but I am too scared to change it
    current_group_student_count = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='list_of_groups_that_the_student_is_in')
    color = models.CharField(max_length=100, blank=False, default='blue', null=True)
    student_projects = models.ManyToManyField(Project, blank=True, related_name='list_of_student_projects_current')
    current_group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='the_current_group_of_the_student')

    def __str__(self):
        return self.user.username


