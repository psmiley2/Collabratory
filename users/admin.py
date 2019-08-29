from django.contrib import admin

from .models import Project, Group, UserInfo
# Register your models here.
admin.site.register(Project)
admin.site.register(Group)
admin.site.register(UserInfo)
