from django.db.models.signals import pre_save
from django.dispatch import receiver

from project.models import AuditHistory, Task


@receiver(pre_save, sender=Task)
def task_edit_history(sender, instance, *args, **kwargs):
    if instance.id:
        previous = Task.objects.get(id=instance.id)
        current = instance
        if previous.name != current.name:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task name changed from {previous.name} to "
                f"{current.name} by {current.updated_by.username} at",
            )
            audit_history.save()
        if previous.assign != current.assign:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task assignee changed from {previous.assign} to "
                f"{current.assign} by {current.updated_by.username} at",
            )
            audit_history.save()
        if previous.task_type != current.task_type:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task type changed from {previous.task_type} to "
                f"{current.task_type} by {current.updated_by.username} at",
            )
            audit_history.save()
        if previous.description != current.description:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task description changed by "
                       f"{current.updated_by.username} at",
            )
            audit_history.save()
        if previous.task_status != current.task_status:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task status changed from {previous.task_status} to "
                f"{current.task_status} by {current.updated_by.username} at",
            )
            audit_history.save()
