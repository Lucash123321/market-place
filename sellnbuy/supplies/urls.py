from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('<str:username>/', views.profile, name='profile')
    ]
