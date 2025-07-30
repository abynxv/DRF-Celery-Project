from django.contrib import admin
from .models import TaskResult, EmailTask


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'task_name', 'created_at')
    search_fields = ('task_id', 'task_name')
    readonly_fields = ('task_id', 'created_at', 'updated_at')
    
    def has_add_permission(self, request):
        return False  # Tasks are created programmatically

@admin.register(EmailTask)
class EmailTaskAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'subject', 'is_sent', 'task_id', 'created_at')
    list_filter = ('is_sent', 'created_at')
    search_fields = ('recipient', 'subject', 'task_id')
    readonly_fields = ('task_id', 'created_at')