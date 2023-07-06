from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, LoginView, \
    LogoutView

app_name = "users"

urlpatterns = [
    path('sign-up', views.SignUp.as_view(), name='sign_up'),
    path('password-reset', PasswordResetView.as_view(template_name="users/password_reset.html", success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password-reset-done', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('password-reset-confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    ]