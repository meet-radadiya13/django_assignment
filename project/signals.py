from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from project.models import AuditHistory, Task


@receiver(post_save, sender=Task)
def task_add_history(sender, instance, *args, **kwargs):
    audit = AuditHistory.objects.last()
    if audit.task is None:
        current = instance
        audit.task = current
        audit.action_by = current.updated_by
        audit.action = f'Task {current.name} created by {current.created_by.username} at {current.created_at}.'
        audit.save()


@receiver(pre_save, sender=Task)
def task_edit_history(sender, instance, *args, **kwargs):
    if instance.id is None:
        current = instance
        audit_history = AuditHistory(
            project=current.project,
        )
        audit_history.save()
    else:
        previous = Task.objects.filter(id=instance.id)
        if len(previous) == 1:
            current = instance
            if previous[0].name != current.name:
                audit_history = AuditHistory(
                    task=current,
                    project=current.project,
                    action_by=current.updated_by,
                    action=f'Task name changed from {previous[0].name} to {current.name} by {current.updated_by.username} at {current.updated_at}.'
                )
                audit_history.save()
            if previous[0].assign != current.assign:
                audit_history = AuditHistory(
                    task=current,
                    project=current.project,
                    action_by=current.updated_by,
                    action=f'Task assignee changed from {previous[0].assign} to {current.assign} by {current.updated_by.username} at {current.updated_at}.'
                )
                audit_history.save()
            if previous[0].task_type != current.task_type:
                audit_history = AuditHistory(
                    task=current,
                    project=current.project,
                    action_by=current.updated_by,
                    action=f'Task type changed from {previous[0].task_type} to {current.task_type} by {current.updated_by.username} at {current.updated_at}.'
                )
                audit_history.save()
            if previous[0].description != current.description:
                audit_history = AuditHistory(
                    task=current,
                    project=current.project,
                    action_by=current.updated_by,
                    action=f'Task description changed by {current.updated_by.username} at {current.updated_at}.'
                )
                audit_history.save()
            if previous[0].task_status != current.task_status:
                audit_history = AuditHistory(
                    task=current,
                    project=current.project,
                    action_by=current.updated_by,
                    action=f'Task status changed from {previous[0].task_status} to {current.task_status} by {current.updated_by.username} at {current.updated_at}.'

                )
                audit_history.save()
