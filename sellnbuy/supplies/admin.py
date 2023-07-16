from django.contrib import admin
from .models import Supply, Comment, Message


# Register your models here.
class SupplyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'desc')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'supply', 'text')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'to', 'text')


admin.site.register(Supply, SupplyAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)
