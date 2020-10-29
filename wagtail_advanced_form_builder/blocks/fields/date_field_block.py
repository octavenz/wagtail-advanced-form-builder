from wagtail.core import blocks

from .base_field_block import BaseFieldBlock


class DateFieldBlock(BaseFieldBlock):

    html = None

    choices = None

    empty_label = None

    display_side_by_side = None

    display_checkbox_label = None

    max_length = None

    default_value = blocks.DateBlock(
        required=False,
        help_text='Choose a default date to populate the date field with.',
    )

    class Meta:

        form_classname = 'waf--field'
        icon = 'extraicons--date'
