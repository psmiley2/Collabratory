from django import forms
from users.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'max_group_size',
            'total_students',
            'project_code',
            'directions',
        ]
