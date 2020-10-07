from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class HiddenFieldBlock(BaseFieldBlock):

    default_value = blocks.CharBlock(
        max_length=255,
        required=True,
    )

    choices = None

    required = None

    help_text = None

    html = None

    display_checkbox_label = None

    empty_label = None

    max_length = None

    display_side_by_side = None

    placeholder = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--hidden'

