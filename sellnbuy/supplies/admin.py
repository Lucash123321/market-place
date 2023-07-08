from django.contrib import admin
from .models import Supply


# Register your models here.
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'desc')


admin.site.register(Supply, SupplyAdmin)
