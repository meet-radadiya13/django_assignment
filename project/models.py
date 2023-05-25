from django.contrib.postgres.fields import ArrayField
from django.db import models

from authentication.models import User


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(CommonModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    acronym = models.CharField(max_length=3, blank=True, null=True)  # api level
    assign = models.ManyToManyField(User, blank=True)
    is_completed = models.BooleanField(default=False)
    dead_line = models.DateField(blank=True, null=True)
    # company = models.ForeignKey('appname.Company', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="project_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="project_updated_by",
    )


class Task(CommonModel):
    CHOICES = [
        ("task", "Task"),
        ("bug", "Bug"),
    ]
    STATUS_CHOICES = [
        ("todo", "TODO"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]
    PRIORITY_CHOICES = [
        ("hi", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    assign = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    task_acronym = models.CharField(max_length=100, blank=True, null=True)
    task_type = models.CharField(choices=CHOICES, default="task")
    task_status = models.CharField(choices=STATUS_CHOICES, default="todo")
    task_priority = models.CharField(choices=PRIORITY_CHOICES, default="medium")
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="task_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="task_updated_by",
    )
    # attachments = GenericRelation(Attachment, object_id_field='object_id', content_type_field='content_type',
    #                               related_query_name='%(app_label)s_%(class)s_content_object', null=True, blank=True)


class Attachment(CommonModel):
    document_name = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to="attachments/", null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    task = models.ForeignKey(
        Task,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks_attachments",
    )
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="attachment_created_by",
    )
    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING,
        related_name="attachment_updated_by",
    )


class AuditHistory(CommonModel):
    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.DO_NOTHING
    )
    action = models.TextField(null=True, blank=True)
    action_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # created_by = models.ForeignKey(
    #     User,
    #     blank=True,
    #     null=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name="audit_created_by",
    # )
    # updated_by = models.ForeignKey(
    #     User,
    #     blank=True,
    #     null=True,
    #     on_delete=models.DO_NOTHING,
    #     related_name="audit_updated_by",
    # )

    class Meta:
        db_table = "audit_history"
