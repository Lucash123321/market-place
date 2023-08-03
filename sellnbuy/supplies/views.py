from django.shortcuts import render, get_object_or_404, redirect
from .models import Supply, User, Comment, Message
from .forms import SupplyForm, CommentForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from . import utils
from django.core.exceptions import PermissionDenied


def main(request):
    paginator = Paginator(Supply.objects.all().order_by('id'), 20)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)
    paginator_page_numbers = [i for i in range(int(page_number) - 2, int(page_number) + 3)]
    context = {"page_obj": page_obj, "paginator_page_numbers": paginator_page_numbers, }
    return render(request, "supplies/index.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    paginator = Paginator(Supply.objects.filter(user=user.id).order_by('id'), 20)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)
    paginator_page_numbers = [i for i in range(int(page_number) - 2, int(page_number) + 3)]
    context = {"page_obj": page_obj, "user": user, "paginator_page_numbers": paginator_page_numbers}
    return render(request, "supplies/profile.html", context)


def view_supply(request, id):
    form = CommentForm()
    supply = get_object_or_404(Supply, id=id)
    paginator = Paginator(Comment.objects.filter(supply=supply).order_by('-id'), 20)
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)
    paginator_page_numbers = [i for i in range(int(page_number) - 2, int(page_number) + 3)]
    is_user_comment_exists = bool(Comment.objects.filter(supply=supply, user=request.user))
    context = {
        "supply": supply,
        "form": form,
        "page_obj": page_obj,
        "paginator_page_numbers": paginator_page_numbers,
        "is_user_comment_exists": is_user_comment_exists,
    }
    return render(request, "supplies/supply_page.html", context)


@login_required
def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            supply = form.save(commit=False)
            supply.user = request.user
            supply.save()
            return redirect('supplies:profile', supply.user)
        print(form.errors)
        return render(request, 'supplies/add_supply.html', {"form": form, 'change': False})
    form = SupplyForm()
    return render(request, 'supplies/add_supply.html', {"form": form, 'change': False})


@login_required
def add_comment(request, id):
    supply = get_object_or_404(Supply, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid() and request.user != supply.user and not Comment.objects.filter(user=request.user,
                                                                                          supply=supply):
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
        if form.is_valid() and request.user.username != username:
            message = form.save(commit=False)
            message.user = request.user
            message.to = to
            message.save()
    return redirect('supplies:chat', username)


@login_required
def open_chat(request, username):
    if request.user.username != username:
        to = get_object_or_404(User, username=username)
        form = MessageForm
        messages = utils.Chat(request.user, to).list_of_messages()
        context = {'messages': messages, 'form': form, 'username': username}
        return render(request, 'supplies/chat.html', context)


@login_required
def messanger(request):
    users = set(Message.objects.filter(user=request.user).values_list('to__username', flat=True))
    chat = {}
    chats = []
    for user in users:
        user = User.objects.get(username=user)
        chat['user'] = user.username
        chat['last_message'] = utils.Chat(request.user.id, user.id).get_last_message()
        chats.append(chat)
        chat = {}
    chats.sort(key=lambda chat: chat['last_message'].time.timestamp(), reverse=True)
    return render(request, 'supplies/messanger.html', {'chats': chats})


@login_required
def change_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user.id == comment.user.id:
        form = CommentForm(request.POST or None, instance=comment)
        if request.method == "POST":
            if form.is_valid():
                form.save()
            return redirect('supplies:supply', comment.supply.id)
        return render(request, 'supplies/change_comment.html', {"form": form})
    raise PermissionDenied()


@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user.id == comment.user.id:
        Comment.objects.filter(id=id).delete()
    return redirect('supplies:supply', comment.supply.id)


@login_required
def change_supply(request, id):
    supply = get_object_or_404(Supply, id=id)
    if request.user.id == supply.user.id:
        form = SupplyForm(request.POST or None, files=request.FILES or None, instance=supply)
        if request.method == "POST":
            if form.is_valid():
                form.save()
            return redirect('supplies:supply', supply.id)
        return render(request, 'supplies/add_supply.html', {"form": form, 'change': True})
    raise PermissionDenied()


@login_required()
def delete_supply(request, id):
    supply = get_object_or_404(Supply, id=id)
    if request.user.id == supply.user.id:
        Supply.objects.filter(id=id).delete()
        return redirect('supplies:profile', supply.user.username)
    return redirect('supplies:supply', supply.id)
