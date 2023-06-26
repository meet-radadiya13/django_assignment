from django.contrib import admin
from related_admin import RelatedFieldAdmin

from authentication.models import Company, PaymentHistory, User
from project.models import Attachment, AuditHistory, Project, Task


# Register your models here.


class CommonModelAdmin(RelatedFieldAdmin):
    readonly_fields = ("created_at", "updated_at")


class ProjectAdmin(CommonModelAdmin, RelatedFieldAdmin):
    list_filter = [
        "is_completed",
        "tags",
        "created_by",
        "dead_line",
    ]
    search_fields = [
        "name",
        "tags",
        "assign",
    ]
    list_display = [
        "name",
        "tags",
        "created_by",
        "dead_line",
    ]


class TaskAdmin(CommonModelAdmin, RelatedFieldAdmin):
    list_filter = [
        "project__name",
        "task_type",
        "task_status",
        "task_priority",
    ]
    search_fields = [
        "name",
        "project__name",
        "assign",
    ]
    list_display = [
        "name",
        "project__name",
        "assign",
        "created_by",
        "task_type",
        "task_status",
        "task_priority",
    ]


class AttachmentAdmin(CommonModelAdmin, RelatedFieldAdmin):
    list_filter = [
        "is_deleted",
        "task__name",
    ]
    search_fields = [
        "document_name",
        "task__name",
    ]
    list_display = [
        "document_name",
        "task__name",
        "created_by",
    ]


class AuditHistoryAdmin(CommonModelAdmin, RelatedFieldAdmin):
    list_filter = [
        "task__name",
        "project__name",
        "action_by",
    ]
    search_fields = [
        "task__name",
        "project__name",
    ]
    list_display = [
        "task__name",
        "project__name",
        "action",
    ]

    def get_task(self, obj):
        return obj.task.name


admin.site.register(User)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(AuditHistory, AuditHistoryAdmin)
admin.site.register(Company, CommonModelAdmin)
admin.site.register(PaymentHistory, CommonModelAdmin)
