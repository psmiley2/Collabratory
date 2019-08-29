from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import ToDo
from django.contrib import messages
from .forms import ToDoForm
from users.models import Project, Group, UserInfo
from django.utils import timezone
import datetime

#should only be able to view if user has a group
@login_required(login_url='/login/')
def to_do_list(request):
    student_group = request.user.userinfo.current_group
    group_posts = ToDo.objects.filter(group=student_group, is_completed=False, is_in_progress=False)
    group_posts_in_progress = ToDo.objects.filter(group=student_group, is_completed=False, is_in_progress=True)
    group_posts_completed = ToDo.objects.filter(group=student_group, is_completed=True, is_in_progress=False)
    context = {'group_posts': group_posts, 'group_posts_in_progress': group_posts_in_progress, 'group_posts_completed': group_posts_completed}
    return render(request, 'to_do/index.html', context)

def user_to_do_list(request):
    user_posts = ToDo.objects.filter(user=request.user, is_completed=False, is_in_progress=False)
    user_posts_in_progress = ToDo.objects.filter(user=request.user, is_completed=False, is_in_progress=True)
    user_posts_completed = ToDo.objects.filter(user=request.user, is_completed=True, is_in_progress=False)
    context = {'user_posts': user_posts, 'user_posts_in_progress': user_posts_in_progress, 'user_posts_completed': user_posts_completed}
    return render(request, 'to_do/user_to_dos.html', context)


class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    template_name = 'to_do/to_do_form.html'
    fields = ['title', 'content']
    success_url = '/to_do/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.group = self.request.user.userinfo.current_group
        date = self.request.POST.get('datepicker', None)
        form.instance.due_date = str(date)
        return super().form_valid(form)

class ToDoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ToDo
    template_name = 'to_do/to_do_form.html'
    fields = ['title', 'content', 'due_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        to_do = self.get_object()
        if self.request.user == to_do.user:
            return True
        return False


class ToDoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ToDo
    template_name = 'to_do/to_do_confirm_delete.html'
    success_url = '/to_do/'

    def test_func(self):
        to_do = self.get_object()
        if self.request.user == to_do.user:
            return True
        return False

def in_progress(request, pk):
    post = get_object_or_404(ToDo, pk=pk)
    setattr(post, 'is_in_progress', True)
    setattr(post, 'user', request.user)
    post.save()
    return redirect('/to_do/')

def completed(request, pk):
    post = get_object_or_404(ToDo, pk=pk)
    setattr(post, 'is_in_progress', False)
    setattr(post, 'is_completed', True)
    setattr(post, 'time_completed', timezone.now())
    post.save()
    return redirect('/to_do/')
