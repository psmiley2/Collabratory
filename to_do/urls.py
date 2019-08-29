from django.urls import path, include
from . import views
from .views import completed, in_progress, user_to_do_list, to_do_list, ToDoCreateView, ToDoUpdateView, ToDoDeleteView

app_name  = 'to_do'

urlpatterns = [
    path('', to_do_list, name='index'),
    path('user/', user_to_do_list, name='user_to_do_list'),
    path('add/', ToDoCreateView.as_view(), name='to_do_create'),
    path('<int:pk>/update/', ToDoUpdateView.as_view(), name='to_do_update'),
    path('<int:pk>/delete/', ToDoDeleteView.as_view(), name='to_do_delete'),
    path('<int:pk>/in_progress/', in_progress, name='in_progress'),
    path('<int:pk>/completed/', completed, name='completed'),

]
