from django.shortcuts import render, get_object_or_404, redirect
from .models import Supply, User, Comment
from .forms import SupplyForm, CommentForm
from django.contrib.auth.decorators import login_required


def main(request):
    context = {"supplies": Supply.objects.all(), }
    return render(request, "supplies/index.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {"supplies": Supply.objects.filter(user=user.id), "user": user}
    return render(request, "supplies/profile.html", context)


def view_supply(request, id):
    form = CommentForm()
    supply = get_object_or_404(Supply, id=id)
    comments = Comment.objects.filter(supply=supply)
    context = {"supply": supply, "form": form, "comments": comments}
    return render(request, "supplies/supply_page.html", context)


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


@login_required
def add_comment(request, id):
    supply = get_object_or_404(Supply, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid() and request.user != supply.user and not Comment.objects.get(user=request.user):
            comment = form.save(commit=False)
            comment.user = request.user
            comment.supply = supply
            comment.save()
    return redirect('supplies:supply', id)




