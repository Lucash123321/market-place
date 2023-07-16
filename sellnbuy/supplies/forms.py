from django import forms
from .models import Supply, Comment, Message


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ('name', 'price', 'desc', )
        labels = {
            'name': 'Название товара',
            'price': 'Цена товара',
            'desc': 'Описание товара'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        labels = {
            'text': 'Введите комментарий'
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )
        labels = {
            'text': 'Отправить сообщение пользователю',
        }
