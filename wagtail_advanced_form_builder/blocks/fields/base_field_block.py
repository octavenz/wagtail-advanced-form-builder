from django import forms
from django.templatetags.static import static

from wagtail.core import blocks
from wagtail.core.blocks import RichTextBlock

from .conditional_block import ConditionalBlock


class BaseFieldBlock(blocks.StructBlock):

    label = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text='The label of the form field.'
    )

    required = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text='Tick this box to make this a required field.'
    )

    display_checkbox_label = blocks.BooleanBlock(
        default=False,
        required=False,
        help_text='Do you want the checkbox label to display? If not you should populate help_text.'
    )

    choices = blocks.ListBlock(
        blocks.TextBlock(
            required=False,
        ),
    )

    empty_label = blocks.CharBlock(
        max_length=255,
        required=False,
    )

    max_length = blocks.IntegerBlock(
        required=False,
        help_text='Set a maximum length for this field. e.g. 100'
    )

    default_value = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text='Set a default value for this field.'
    )

    # placeholder = blocks.CharBlock(
    #     max_length=255,
    #     required=False,
    #     help_text='Set a placeholder for the field.'
    # )

    help_text = blocks.CharBlock(
        max_length=255,
        required=False,
        help_text='Text to assist the user in populating this field.'
    )

    html = RichTextBlock(
        required=False,
    )

    display_side_by_side = blocks.BooleanBlock(
        help_text='Display these items side by side?',
        required=False,
    )

    rules = ConditionalBlock(
        required=False,
        help_text='Add conditional rules to show or hide fields depending on the value of other fields in the form.'
    )

    @property
    def media(self):
        return forms.Media(js=[static('wagtail_advanced_form_builder/js/admin.js')])
