from django.contrib import admin

from .models import Project, Task

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "is_completed", "due_date")
    list_filter = ("is_completed", "due_date")