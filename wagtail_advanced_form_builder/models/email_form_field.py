from django.db import models
from modelcluster.fields import ParentalKey

from .abstract_advanced_form_field import AbstractAdvancedFormField


class EmailFormField(AbstractAdvancedFormField):

    page = ParentalKey(
        'wagtail_advanced_form_builder.EmailFormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
