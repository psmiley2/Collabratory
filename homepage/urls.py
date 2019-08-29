from django.urls import path, include
from . import views

app_name  = 'homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('find_project/', views.find_project, name='find_project'),
    path('directions/', views.directions, name='directions'),
    path('add_group/<int:pk>/', views.add_group, name='add_group'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/join/', views.join_project, name='join_project'),
    path('projects/<int:pk>/confirm_join/', views.confirm_join, name='confirm_join'),
   path('<int:project_id>/join_group/<int:pk>/', views.join_group, name='join_group'),
    path('<int:project_id>/view_group/<int:pk>/', views.view_group, name='view_group'),
    path('<int:student_pk>/remove_from_group/<int:group_pk>/', views.remove_from_group, name='remove_from_group'),
    path('<int:student_pk>/remove_from_project/<int:group_pk>/', views.remove_from_project, name='remove_from_project'),
   path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
   path('<int:pk>/group_delete/', views.GroupDeleteView.as_view(), name='group_delete'),
   path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
   path('<int:project_pk>/completed/', views.project_completed, name='project_completed'),
   path('<int:project_pk>/restore/', views.project_restore, name='project_restore'),

]
