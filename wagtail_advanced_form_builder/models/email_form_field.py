from django.db import models
from modelcluster.fields import ParentalKey
from django.conf import settings

from .abstract_advanced_form_field import AbstractAdvancedFormField

DEFAULT_EMAIL_FORM_PAGE_MODEL = 'wagtail_advanced_form_builder.EmailFormPage'


class EmailFormField(AbstractAdvancedFormField):

    page = ParentalKey(
        getattr(settings, 'ADVANCED_FORMS_EMAIL_FORM_PAGE_MODEL', DEFAULT_EMAIL_FORM_PAGE_MODEL),
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
