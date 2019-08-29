from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Project, Group, UserInfo
from django.contrib import messages
from .forms import ProjectForm
import math
from django.db.models import F
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/index.html', {'logged_in': False})
    if request.user.userinfo.is_teacher == True:
        form = ProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.teacher = request.user
            instance.save()
            messages.success(request, "Successfully Created")
            return redirect('/')
        return render(request, 'homepage/index.html', {'form': form, 'logged_in': True})
    elif request.user.userinfo.is_teacher == False:
        all_projects = Project.objects.all()
        return render(request, 'homepage/index.html', {'all_projects': all_projects, 'logged_in': True})
    return render(request, 'homepage/index.html')

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'homepage/teacher_home.html'
    fields = ['title', 'max_group_size', 'total_students']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    template_name = 'homepage/project_form.html'
    fields = ['title', 'max_group_size', 'total_students', 'project_code', 'directions']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.teacher:
            return True
        return False

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'homepage/project_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        project = self.get_object()
        if self.request.user == project.teacher:
            return True
        return False

class GroupDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group
    template_name = 'homepage/group_confirm_delete.html'

    def get_success_url(self):
        group = self.get_object()
        project = group.project
        my_pk = str(project.pk)
        return f'/projects/{my_pk}/'

    def test_func(self):
        group = self.get_object()
        if self.request.user == group.project.teacher:
            return True
        return False


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    context = {'project': project}
    all_student_groups = request.user.userinfo.groups.all()
    for student_group in all_student_groups:
        if student_group in project.projects_associated_with_group.all():
            context.update({'student_group' : student_group})
            setattr(request.user.userinfo, 'current_group', student_group)
            request.user.userinfo.save()
    return render(request, 'homepage/project_detail.html', context)

def find_project(request):
    all_projects = Project.objects.all()
    all_codes = Project.objects.values_list('project_code', flat=True)
    code = ''
    x = 0
    if request.method == "POST":
        code=request.POST.get('project_code', False)
        if code in all_codes:
            x = list(all_codes).index(code)
            all_projects_list = list(all_projects)

            #give user permission to look at the groups in the project -> write later
            if all_projects_list[x] in request.user.userinfo.student_projects.all():
                return redirect(f'/projects/{all_projects_list[x].pk}/')
            return redirect(f'/projects/{all_projects_list[x].pk}/join/')

    context = {'code': code, 'all_projects': all_projects, 'all_codes':all_codes, 'x':x}
    return redirect('/')

def join_group(request, project_id, pk):
    new_group = get_object_or_404(Group, pk=pk)
    request.user.userinfo.groups.add(new_group)
    Group.objects.filter(pk=pk).update(current_group_student_count=F('current_group_student_count')+1)
    #setattr(request.user.userinfo, 'groups', new_group)
    #request.user.userinfo.groups.save()
    return redirect(f'/projects/{project_id}')

def view_group(request, project_id, pk):
    new_group = get_object_or_404(Group, pk=pk)
    setattr(request.user.userinfo, 'current_group', new_group)
    request.user.userinfo.save()
    return redirect(f'/projects/{project_id}')

@login_required(login_url='/login/')
def directions(request):
    return render(request, 'homepage/directions.html')

def add_group(request, pk):
    new_project = get_object_or_404(Project, pk=pk)
    new_group = request.POST.get('new_group', False)
    Group.objects.create(title=new_group, project=new_project)
    return redirect(f'/projects/{pk}/')

def join_project(request, pk):
    new_project = get_object_or_404(Project, pk=pk)
    context = {'new_project': new_project}
    if new_project.total_students == new_project.current_project_student_count:
        context.update( {'is_full' : True} )
    return render(request, 'homepage/join_project_confirm.html', context)

def confirm_join(request, pk):
    new_project = get_object_or_404(Project, pk=pk)
    user_projects = request.user.userinfo.student_projects
    user_projects.add(new_project)
    Project.objects.filter(pk=pk).update(current_project_student_count=F('current_project_student_count')+1)
    return redirect(f'/projects/{pk}/')

def remove_from_group(request, student_pk, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(UserInfo, pk=student_pk)
    current_project = group.project
    if student.current_group == group:
        setattr(student, 'current_group', None)
        student.save()
    Group.objects.filter(pk=group.pk).update(current_group_student_count=F('current_group_student_count')-1)
    student.groups.remove(group)
    return redirect(f'/projects/{current_project.pk}/')


def remove_from_project(request, student_pk, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    project = group.project
    student = get_object_or_404(UserInfo, pk=student_pk)
    if student.current_group == group:
        setattr(student, 'current_group', None)
        student.save()
    Project.objects.filter(pk=project.pk).update(current_project_student_count=F('current_project_student_count')-1)
    Group.objects.filter(pk=group.pk).update(current_group_student_count=F('current_group_student_count')-1)
    student.groups.remove(group)
    student.student_projects.remove(project)
    return redirect(f'/projects/{project.pk}/')

def project_completed(request, project_pk):
    proj = get_object_or_404(Project, pk=project_pk)
    setattr(proj, 'is_completed', True)
    proj.save()
    return redirect('/')

def project_restore(request, project_pk):
    proj = get_object_or_404(Project, pk=project_pk)
    setattr(proj, 'is_completed', False)
    proj.save()
    return redirect('/')
