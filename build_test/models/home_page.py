from wagtail.core.models import Page


class HomePage(Page):
    subpage_types = [
        'wagtail_advanced_form_builder.EmailFormPage',
        'wagtail_advanced_form_builder.FormPage',
    ]
