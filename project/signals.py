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
                action=f"Task name changed from "
                       f"{previous.name} to {current.name}",
            )
            audit_history.save()
        if previous.assign != current.assign:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action="Task assignee changed",
                user_from=previous.assign,
                user_to=current.assign
            )
            audit_history.save()
        if previous.task_type != current.task_type:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task type changed from "
                       f"{previous.task_type} to {current.task_type}",
            )
            audit_history.save()
        if previous.description != current.description:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action="Task description changed",
            )
            audit_history.save()
        if previous.task_status != current.task_status:
            audit_history = AuditHistory(
                task=current,
                project=current.project,
                action_by=current.updated_by,
                action=f"Task status changed from "
                       f"{previous.task_status} to {current.task_status}",
            )
            audit_history.save()

