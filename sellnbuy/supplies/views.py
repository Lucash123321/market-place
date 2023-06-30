from django.shortcuts import render
from .models import Supply


def main(request):
    context = {"supplies": Supply.objects.all(), }
    return render(request, "supplies/index.html", context)