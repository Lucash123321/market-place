from . import views
from django.urls import path

app_name = 'about'

urlpatterns = [
    path('about-author', views.author_page, name='author_page'),
    path('techs', views.techs, name='techs')
]