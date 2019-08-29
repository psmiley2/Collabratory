from django import forms
from .models import ToDo
from django.contrib.admin import widgets

class ToDoForm(forms.ModelForm):

    class Meta:
        model = ToDo
        fields = [
            'title',
            'content',
            'due_date',
            'group',
        ]
