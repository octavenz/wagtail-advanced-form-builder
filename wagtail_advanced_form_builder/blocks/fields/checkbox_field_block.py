from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class CheckboxFieldBlock(BaseFieldBlock):

    choices = None

    help_text = blocks.CharBlock(
        max_length=255,
        required=False,
    )

    html = None

    default_value = None

    display_side_by_side = None

    empty_label = None

    max_length = None

    placeholder = None


    class Meta:

        form_classname = 'waf--field'
        icon = 'extraicons--checkbox'
