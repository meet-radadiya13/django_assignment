from django.contrib import admin

from authentication.models import User
from project.models import Task, Attachment, AuditHistory


# Register your models here.

class CommonModelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')


class ProjectAdmin(CommonModelAdmin, admin.ModelAdmin):
    list_filter = [
        'is_completed',
        'tags',
        'created_by',
        'deadline',
    ]
    search_fields = [
        'name',
        'tags',
        'assign',
    ]
    list_display = [
        'name',
        'tags',
        'created_by',
        'deadline',
        'assign',
    ]


class TaskAdmin(CommonModelAdmin, admin.ModelAdmin):
    list_filter = [
        'project',
        'task_type',
        'task_status',
        'task_priority',
    ]
    search_fields = [
        'name',
        'project',
        'assign',
    ]
    list_display = [
        'name',
        'project',
        'assign',
        'created_by',
        'task_type',
        'task_status',
        'task_priority',
    ]


class AttachmentAdmin(CommonModelAdmin, admin.ModelAdmin):
    list_filter = [
        'is_deleted',
        'task',
    ]
    search_fields = [
        'document_name',
        'task',
    ]
    list_display = [
        'document_name',
        'task',
        'created_by',
    ]


class AuditHistoryAdmin(CommonModelAdmin, admin.ModelAdmin):
    list_filter = [
        'task',
        'project',
        'action_by',
    ]
    search_fields = [
        'task',
        'project',
    ]
    list_display = [
        'task',
        'project',
        'action',
        'created_by',
    ]


admin.site.register(User)
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(AuditHistory, AuditHistoryAdmin)
