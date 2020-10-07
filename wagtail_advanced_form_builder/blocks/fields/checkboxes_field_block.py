from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class CheckboxesFieldBlock(BaseFieldBlock):

    choices = blocks.ListBlock(
        blocks.TextBlock(
            required=True,
            icon='extraicons--heading-icon',
        ),
    )

    default_value = blocks.ListBlock(
        blocks.TextBlock(
            required=True,
            icon='extraicons--heading-icon',
            help_text='Enter a value that matches a checkbox choice above to have it ticked by default.'
        ),
    )

    html = None

    empty_label = None

    max_length = None

    placeholder = None

    display_checkbox_label = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--checkboxes'
