from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_password_reset_email_task(subject, message, recipient):
    """
    Sends a password reset email asynchronously.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending password reset email via Celery: {e}")

@shared_task
def send_registration_success_email_task(recipient, name):
    """
    Sends a welcome email after successful registration asynchronously.
    """
    subject = "Welcome to Crumbs!"
    message = f"Hello {name},\n\nWelcome to Crumbs! We are excited to have you on board.\n\nBest regards,\nThe Crumbs Team"
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending registration success email via Celery: {e}")

@shared_task
def send_login_success_email_task(recipient, name):
    """
    Sends a notification email after a successful login asynchronously.
    """
    subject = "New Login to Your Crumbs Account"
    message = f"Hello {name},\n\nWe noticed a successful login to your Crumbs account just now. If this was you, you don't need to do anything.\n\nIf you didn't log in recently, please reset your password immediately.\n\nBest regards,\nThe Crumbs Team"
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending login success email via Celery: {e}")
