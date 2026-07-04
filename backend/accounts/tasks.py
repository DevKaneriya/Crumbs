import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def _send_mail_safe(subject, message, recipient):
    """
    Wrapper around send_mail that catches all exceptions so a mail failure
    never crashes the calling view.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        logger.info('Email sent to %s — subject: %s', recipient, subject)
    except Exception as exc:
        logger.error('Failed to send email to %s — %s: %s', recipient, type(exc).__name__, exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, subject, message, recipient):
    """Sends a password reset email. Retries up to 3 times on failure."""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        logger.info('Password reset email sent to %s', recipient)
    except Exception as exc:
        logger.error('Password reset email failed for %s: %s', recipient, exc)
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error('Max retries exceeded for password reset email to %s', recipient)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_registration_success_email_task(self, recipient, name):
    """Sends a welcome email after registration. Retries up to 3 times on failure."""
    subject = "Welcome to Crumbs!"
    message = (
        f"Hello {name},\n\n"
        "Welcome to Crumbs! We are excited to have you on board.\n\n"
        "Best regards,\nThe Crumbs Team"
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        logger.info('Welcome email sent to %s', recipient)
    except Exception as exc:
        logger.error('Welcome email failed for %s: %s', recipient, exc)
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error('Max retries exceeded for welcome email to %s', recipient)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_login_success_email_task(self, recipient, name):
    """Sends a login notification email. Retries up to 3 times on failure."""
    subject = "New Login to Your Crumbs Account"
    message = (
        f"Hello {name},\n\n"
        "We noticed a successful login to your Crumbs account just now. "
        "If this was you, you don't need to do anything.\n\n"
        "If you didn't log in recently, please reset your password immediately.\n\n"
        "Best regards,\nThe Crumbs Team"
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        logger.info('Login notification email sent to %s', recipient)
    except Exception as exc:
        logger.error('Login notification email failed for %s: %s', recipient, exc)
        try:
            raise self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            logger.error('Max retries exceeded for login email to %s', recipient)
