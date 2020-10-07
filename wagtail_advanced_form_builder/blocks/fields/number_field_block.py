from .base_field_block import BaseFieldBlock


class NumberFieldBlock(BaseFieldBlock):

    choices = None

    html = None

    display_checkbox_label = None

    empty_label = None

    display_side_by_side = None

    placeholder = None

    max_length = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--number'
