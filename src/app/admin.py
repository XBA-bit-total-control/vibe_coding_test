from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "status", "owner", "created_at"]
    list_filter = ["title"]
    search_fields = ["title", "status", "owner"]
    ordering = ["id"]
