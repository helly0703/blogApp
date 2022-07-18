from django import forms
from django.contrib import admin

# Register your models here.

from chat.models import ChatMessage, Thread

admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage


class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
