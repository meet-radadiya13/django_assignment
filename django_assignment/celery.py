import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_assignment.settings')

app = Celery('django_assignment')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'schedule-alert-email': {
        'task': 'django_assignment.task.mail_scheduler',
        'schedule': timedelta(minutes=10),
        'args': ()
    }
}
