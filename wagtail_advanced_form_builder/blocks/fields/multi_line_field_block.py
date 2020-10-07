from .base_field_block import BaseFieldBlock


class MultiLineFieldBlock(BaseFieldBlock):

    choices = None

    html = None

    buttons_style = None

    display_checkbox_label = None

    empty_label = None

    max_length = None

    display_side_by_side = None

    placeholder = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--text-box'
