from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class DropdownFieldBlock(BaseFieldBlock):

    choices = blocks.ListBlock(
        blocks.TextBlock(
            required=True,
            icon='extraicons--heading-icon',
        ),
    )

    html = None

    max_length = None

    placeholder = None

    display_side_by_side = None

    display_checkbox_label = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--dropdown'
