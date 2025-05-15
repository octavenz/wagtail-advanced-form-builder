from wagtail import blocks

from .base_field_block import BaseFieldBlock


class SimpleDateFieldBlock(BaseFieldBlock):
    # Reason for this block called SimpleDateFieldBlock due to usage of CharBlock for default_value instead of Date select widget

    choices = None

    html = None

    empty_label = None

    default_value = blocks.CharBlock(
        max_length=10,
        required=False,
        help_text='dd/mm/yyyy e.g. 19/08/1981'
    )

    buttons_style = None

    display_checkbox_label = None

    display_side_by_side = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--date'
