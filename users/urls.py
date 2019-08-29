from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change_color/<str:color_name>/', views.color_changer, name='color_changer'),
]
