from django.contrib import admin
from .models import Supply, Comment


# Register your models here.
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'desc')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'supply', 'text')


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Comment, CommentAdmin)
