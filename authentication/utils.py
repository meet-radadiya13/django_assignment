from datetime import datetime, timedelta

import stripe
from django.core import mail

from django_assignment import settings


def send_registration_mail(email, password, company, firstname, uri, ):
    connection = mail.get_connection()
    subject = "Welcome to " + company + ", " + firstname + " !"
    message = "We are glad to have you here! \n" \
              "Your credentials are \nEmail: " \
              + email + "\nPassword: " + password + "\n" + \
              "You can login on \n" + uri
    email = mail.EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        connection=connection,
    )
    email.send()


def check_subscription(request):
    subscription = stripe.Subscription.retrieve(
        request.user.stripe_subscription_id
    )
    if subscription.status == 'active':
        current_period_end_date = datetime.fromtimestamp(
            subscription.current_period_end
        )
        return current_period_end_date - datetime.now() <= timedelta(days=3)
