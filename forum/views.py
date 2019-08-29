from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.contrib import messages
from .forms import PostForm, CommentForm
from users.models import Project, Group, UserInfo
from django.utils import timezone

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    student_group = request.user.userinfo.current_group
    group_posts = Post.objects.filter(group=student_group).order_by('id')
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.group = request.user.userinfo.current_group
        instance.save()
        messages.success(request, "Successfully Created")
        return redirect('/forum/')
    context = {'group_posts': group_posts, 'form': form}
    return render(request, 'forum/index.html', context)

@login_required(login_url='/login/')
def comment_create(request, post_pk):
    form = CommentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        _post = get_object_or_404(Post, pk=post_pk)
        instance.post = _post
        instance.save()
        messages.success(request, "Successfully Created")
        return redirect('/forum/')
    return render(request, 'forum/comment_form.html', {'form': form})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'forum/comment_confirm_delete.html'
    success_url = '/forum/'

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

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

def make_fullscreen(request, image_pk):
    post = get_object_or_404(Post, pk=image_pk)
    return render(request, 'forum/fullscreen_image.html', {'post': post})
