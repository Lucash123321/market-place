from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        return render(request, 'users/registration.html', {'form': form})
    form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})
