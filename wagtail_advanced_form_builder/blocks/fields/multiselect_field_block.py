from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class MultiSelectFieldBlock(BaseFieldBlock):

    choices = blocks.ListBlock(
        blocks.TextBlock(
            required=True,
            icon='extraicons--heading-icon',
        ),
    )

    html = None

    display_checkbox_label = None

    placeholder = None

    empty_label = None

    max_length = None

    display_side_by_side = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--multi-select'
