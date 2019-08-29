from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from to_do.models import ToDo
from django.contrib import messages
from users.models import Project, Group, UserInfo
from django.utils import timezone


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    student_group = request.user.userinfo.current_group
    group_posts = ToDo.objects.filter(group=student_group, is_completed=False).order_by('due_date')
    context = {'group_posts': group_posts}
    return render(request, 'timeline/index.html', context)

'''
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'forum/post_form.html'
    fields = ['content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'
    success_url = '/forum/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False
'''
