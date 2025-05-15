from .base_field_block import BaseFieldBlock


class PhoneFieldBlock(BaseFieldBlock):

    choices = None

    html = None

    start_year = None

    end_year = None

    buttons_style = None

    display_checkbox_label = None

    empty_label = None

    display_side_by_side = None

    minimum_age = None

    maximum_age = None

    class Meta:

        form_classname = 'waf--field'
        icon = 'extraicons--basic-field'
