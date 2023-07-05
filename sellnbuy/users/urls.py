from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, LoginView

app_name = "users"

urlpatterns = [
    path('sign-up', views.SignUp.as_view(), name='sing-up'),
    path('password-reset', PasswordResetView.as_view(), name='password-reset'),
    path('password-reset-done', PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password-reset-confirm', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('login', LoginView.as_view(template_name="users/login.html"), name='login')
    ]