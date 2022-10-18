from django.db import models

from modelcluster.fields import ParentalKey

from .abstract_advanced_form_field import AbstractAdvancedFormField


class EmailFormField(AbstractAdvancedFormField):

    # Add explicit `id` primary key using Django's defaults for versions
    # prior to 3.2 to avoid migrations when upgrading to that version.
    id = models.AutoField(
        primary_key=True,
        auto_created=True,
        serialize=False,
        verbose_name='ID',
    )
    page = ParentalKey(
        'wagtail_advanced_form_builder.EmailFormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )
