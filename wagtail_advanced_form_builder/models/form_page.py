from wagtail.core.models import Page

from wagtail_advanced_form_builder.models.abstract_advanced_form import AbstractAdvancedForm


class FormPage(AbstractAdvancedForm):

    settings_panels = Page.settings_panels + AbstractAdvancedForm.settings_panels

