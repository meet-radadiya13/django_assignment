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
