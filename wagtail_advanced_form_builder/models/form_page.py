from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from django.db import models

from wagtail_advanced_form_builder.models.abstract_advanced_form import AbstractAdvancedForm


class FormPage(AbstractAdvancedForm):

    use_google_recaptcha = models.BooleanField(
        default=False,
        null=False,
        blank=False,
        help_text='Please tick this option to enable Google Recaptcha'
    )

    content_panels = Page.content_panels + AbstractAdvancedForm.content_panels + [
        FieldPanel('use_google_recaptcha')
    ]

    settings_panels = Page.settings_panels + AbstractAdvancedForm.settings_panels
