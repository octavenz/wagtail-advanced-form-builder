from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class RadioFieldBlock(BaseFieldBlock):

    choices = blocks.ListBlock(
        blocks.TextBlock(
            required=True,
            icon='extraicons--heading-icon',
        ),
    )

    html = None

    empty_label = None

    max_length = None

    placeholder = None

    display_checkbox_label = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--radio'
