from wagtail.core.models import Page

from .abstract_advanced_email_form import AbstractAdvancedEmailForm


class EmailFormPage(AbstractAdvancedEmailForm):

    content_panels = Page.content_panels + AbstractAdvancedEmailForm.content_panels

    settings_panels = Page.settings_panels + AbstractAdvancedEmailForm.settings_panels

