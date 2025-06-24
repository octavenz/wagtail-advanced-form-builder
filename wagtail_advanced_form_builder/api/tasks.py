from celery import shared_task
from celery.utils.log import get_task_logger
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=2, ignore_result=True)
def send_form_page_email(self, email_data):
    try:
        form_title = email_data.get('form_title', '')
        subject = email_data.get('subject', 'Form Submission')
        from_address = email_data.get('from_address', settings.DEFAULT_FROM_EMAIL)
        to_address = email_data.get('to_address', '')
        content = email_data.get('content', {})

        # Processing email template
        form_fields = []
        for key, value in content.items():
            # Skip HTML fields
            if key == 'html-field':
                continue

            # Skip empty values: None, '', [], or {}
            if value in (None, '', [], {}):
                continue

            # Format field name from slug to title
            field_label = key.replace('-', ' ').title()

            # If it's a list, join the string together
            if isinstance(value, list):
                formatted_value = ', '.join(str(v) for v in value if v)
                if not formatted_value:
                    continue  # Skip if list was empty
            else:
                formatted_value = str(value)

            form_fields.append((field_label, formatted_value))

        # Prepare email context data
        email_context = {
            'form_title': form_title,
            'form_fields': form_fields,
        }

        html_content = render_to_string('emails/form_submission.html', email_context)
        plain_content = strip_tags(html_content)

        # Format recipient list of address emails
        recipient_list = [email.strip() for email in to_address.split(',') if email.strip()]

        # Send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_content,
            from_email=from_address,
            to=recipient_list,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        logger.info(f"Email sent successfully to {to_address}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds
        return None
