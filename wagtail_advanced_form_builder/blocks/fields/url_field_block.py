from .base_field_block import BaseFieldBlock


class URLFieldBlock(BaseFieldBlock):

    choices = None

    html = None

    display_checkbox_label = None

    empty_label = None

    display_side_by_side = None

    placeholder = None

    class Meta:
        form_classname = 'waf--field'
        icon = 'extraicons--url'
