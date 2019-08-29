from django.urls import path, include
from . import views

app_name  = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('<int:post_pk>/comment/', views.comment_create, name='comment_create'),
    path('<int:pk>/comment/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('fullscreen/<int:image_pk>/', views.make_fullscreen, name='make_fullscreen'),
]
