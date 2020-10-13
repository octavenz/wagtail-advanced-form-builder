from django.db import models
from modelcluster.fields import ParentalKey
from .abstract_advanced_form_field import AbstractAdvancedFormField


class FormField(AbstractAdvancedFormField):

    page = ParentalKey(
        'wagtail_advanced_form_builder.FormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
