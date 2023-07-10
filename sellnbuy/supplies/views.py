from django.shortcuts import render, get_object_or_404, redirect
from .models import Supply, User
from .forms import SupplyForm
from django.contrib.auth.decorators import login_required


def main(request):
    context = {"supplies": Supply.objects.all(), }
    return render(request, "supplies/index.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {"supplies": Supply.objects.filter(user=user.id), "user": user}
    return render(request, "supplies/profile.html", context)


@login_required
def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST or None)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.user = request.user
            supply.save()
            return redirect('supplies:profile', supply.user)
        return render(request, 'supplies/add_supply.html', {"form": form})
    form = SupplyForm()
    return render(request, 'supplies/add_supply.html', {"form": form})


def view_supply(request, id):
    supply = get_object_or_404(Supply, id=id)
    context = {"supply": supply}
    return render(request, "supplies/supply_page.html", context)
