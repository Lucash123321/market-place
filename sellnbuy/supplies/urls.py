from django.urls import path
from . import views

app_name = "supplies"

urlpatterns = [
    path('', views.main, name='index'),
    path('add-supply/', views.add_supply, name='add_supply'),
    path('<int:id>/', views.view_supply, name='supply'),
    path('<int:id>/comment', views.add_comment, name='add_comment'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/chat', views.open_chat, name='chat'),
    path('<str:username>/chat/send-message', views.send_message, name='send_message'),
    ]
