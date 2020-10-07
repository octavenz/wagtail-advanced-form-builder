from django.db import models
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.fields import RichTextField

import wagtail_advanced_form_builder.constants as consts
from wagtail_advanced_form_builder.utils import clean_form_field_name

OVERRIDE_FORM_FIELD_CHOICES = (
    (consts.FIELD_TYPE_SINGLE_LINE, _('Single line text')),
    (consts.FIELD_TYPE_MULTI_LINE, _('Multi-line text')),
    (consts.FIELD_TYPE_EMAIL, _('Email')),
    (consts.FIELD_TYPE_NUMBER, _('Number')),
    (consts.FIELD_TYPE_URL, _('URL')),
    (consts.FIELD_TYPE_CHECKBOX, _('Checkbox')),
    (consts.FIELD_TYPE_CHECKBOXES, _('Checkboxes')),
    (consts.FIELD_TYPE_DROPDOWN, _('Drop down')),
    (consts.FIELD_TYPE_MULTI_SELECT, _('Multiple select')),
    (consts.FIELD_TYPE_RADIO, _('Radio buttons')),
    (consts.FIELD_TYPE_DATE, _('Date')),
    (consts.FIELD_TYPE_HIDDEN, _('Hidden field')),
    (consts.FIELD_TYPE_CURRENCY, _('Currency field')),
    (consts.FIELD_TYPE_SIMPLE_DATE, _('Date')),
    (consts.FIELD_TYPE_PHONE, _('Phone')),
)


class AbstractAdvancedFormField(AbstractFormField, ClusterableModel):

    # extend the built in field type choices so we can add custom fields
    CHOICES = OVERRIDE_FORM_FIELD_CHOICES

    # override the field_type field with extended choices
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        # use the choices tuple defined above
        choices=CHOICES
    )

    rule_action = models.CharField(
        choices=consts.FIELD_ACTION_CHOICES,
        blank=True,
        default='',
        max_length=10,
    )


    # Storage for HTML field only
    html_value = RichTextField(
        default=None,
        null=True,
        blank=True,
    )

    # Set a maximum length on fields
    max_length = models.IntegerField(
        default=None,
        null=True,
        blank=True,
    )

    # Empty label option for choice fields only
    empty_label = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True,
    )

    # Storage for checkboxes and radios only
    display_side_by_side = models.BooleanField(
        default=False
    )

    display_checkbox_label = models.BooleanField(
        default=False,
    )

    @property
    def clean_name(self):
        return clean_form_field_name(self.label)

    class Meta:
        abstract = True
