from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_review_email(username, email,role):
    print(email)
    email_subject = 'Registration succesfull'
    email_body = f"dear {username},\nYou are succesfully registered in task tracker app as a {role}."

    send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL, 
        recipient_list=[email, ],
        fail_silently=True
    )
    return "DONE"