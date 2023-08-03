from django import forms
from .models import Supply, Comment, Message


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ('name', 'price', 'desc', 'image', )
        labels = {
            'name': 'Название товара',
            'price': 'Цена товара',
            'desc': 'Описание товара',
            'image': 'Фотография товара',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('rating', 'text', )
        labels = {
            'rating': 'Ваша оценка',
            'text': 'Текст комментария',
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )
        labels = {
            'text': 'Отправить сообщение пользователю',
        }
