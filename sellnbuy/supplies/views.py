from django.shortcuts import render, get_object_or_404, redirect
from .models import Supply, User, Comment, Message
from .forms import SupplyForm, CommentForm, MessageForm
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


@login_required
def send_message(request, username):
    to = get_object_or_404(User, username=username)
    if request.method == "POST":
        form = MessageForm(request.POST or None)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.to = to
            message.save()
    return redirect('supplies:chat', username)


@login_required
def open_chat(request, username):
    to = get_object_or_404(User, username=username)
    sent = list(Message.objects.filter(to=to, user=request.user))
    received = list(Message.objects.filter(to=request.user, user=to))
    form = MessageForm
    i, j = 0, 0
    messages = []
    while i < len(sent) or j < len(received):
        if i < len(sent) and j < len(received) and sent[i].id < received[j].id:
            messages.append(sent[i])
            i += 1
        elif i < len(sent) and j < len(received) and sent[i].id > received[j].id:
            messages.append(received[j])
            j += 1
        elif i < len(sent) and j == len(received):
            messages += sent[i:]
            break
        elif j < len(received) and i == len(sent):
            messages += received[j:]
            break
    context = {'messages': messages, 'form': form, 'username': username}
    return render(request, 'supplies/chat.html', context)
