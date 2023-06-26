from datetime import datetime, timedelta

from celery import shared_task
from django.utils import timezone


@shared_task
def send_alert_email():
    print("Alert=========================> Your subscription is about to end")


@shared_task
def mail_scheduler():
    now = timezone.now()
    tomorrow = now + timedelta(days=1)
    run_time = datetime(
        tomorrow.year, tomorrow.month, tomorrow.day,
        hour=0, minute=0, tzinfo=now.tzinfo
        )
    send_alert_email.apply_async(eta=run_time)
