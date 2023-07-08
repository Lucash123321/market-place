from django.shortcuts import render, get_object_or_404
from .models import Supply
from django.contrib.auth.models import User


def main(request):
    context = {"supplies": Supply.objects.all(), }
    return render(request, "supplies/index.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {"supplies": Supply.objects.filter(user=user.id), "user": user}
    return render(request, "supplies/profile.html", context)
