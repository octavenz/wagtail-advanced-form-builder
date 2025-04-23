from celery import shared_task
from celery.utils.log import get_task_logger

from django.core.mail import send_mail
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=2, ignore_result=True)
def send_form_page_email(self, email_data):
    try:
        form_title = email_data.get('form_title')
        subject = email_data.get('subject', 'Form Submission')
        from_address = email_data.get('from_address', settings.DEFAULT_FROM_EMAIL)
        to_address = email_data.get('to_address')
        content = email_data.get('content', {})

        # Format the email content with better spacing and structure
        email_content = f"""
New submission received for {form_title}

Form Details:
"""

        # Add each form field with proper spacing
        for key, value in content.items():
            # Skip empty value and HTML fields
            if key == 'html-field' and not value:
                continue

            # Format field name from slug to title
            field_name = key.replace('-', ' ').title()
            email_content += f"\n{field_name}: {value}"

        # Send the email
        send_mail(
            subject=subject,
            message=email_content,
            from_email=from_address,
            recipient_list=[to_address],
            fail_silently=False,
        )

        logger.info(f"Email sent successfully to {to_address}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds
