from django import forms
from .models import Supply


class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ('name', 'price', 'desc', )
        labels = {
            'name': 'Название товара',
            'price': 'Цена товара',
            'desc': 'Описание товара'
        }
