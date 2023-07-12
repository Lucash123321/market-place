from django.urls import path
from . import views

app_name = "supplies"

urlpatterns = [
    path('', views.main, name='index'),
    path('add-supply/', views.add_supply, name='add_supply'),
    path('<int:id>/', views.view_supply, name='supply'),
    path('<int:id>/comment', views.add_comment, name='add_comment'),
    path('<str:username>/', views.profile, name='profile'),
    ]
