from django.contrib import admin
from .models import Task,Thought

# admin.site.register(Task,Thoughts)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Thought)
class ThoughtsAdmin(admin.ModelAdmin):
    pass