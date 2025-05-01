from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from django.db import models

from .abstract_advanced_email_form import AbstractAdvancedEmailForm


class EmailFormPage(AbstractAdvancedEmailForm):

    use_google_recaptcha = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text='Please tick this option to enable Google Recaptcha'
    )

    content_panels = Page.content_panels + AbstractAdvancedEmailForm.content_panels + [
        FieldPanel('use_google_recaptcha')
    ]

    settings_panels = Page.settings_panels + AbstractAdvancedEmailForm.settings_panels
