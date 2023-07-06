from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.views.generic import CreateView

# Create your views here.


class SignUp(CreateView): #переделать?
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


