from django.urls import path, include
from . import views

app_name  = 'timeline'

urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:pk>/update/', views.GoalUpdateView.as_view(), name='goal_update'),
    #path('<int:pk>/delete/', views.GoalDeleteView.as_view(), name='goal_delete'),
]
