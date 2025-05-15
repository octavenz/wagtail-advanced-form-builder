from wagtail import blocks

from .base_field_block import BaseFieldBlock


class HTMLFieldBlock(BaseFieldBlock):

    label = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text='A unique reference for this html block',
        label='Unique reference name',
    )

    html = blocks.RichTextBlock(
        required=True,
        features=['bold', 'italic', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'link']
    )

    help_text = None

    max_length = None

    required = None

    default_value = None

    placeholder = None

    choices = None

    empty_label = None

    display_side_by_side = None

    display_checkbox_label = None

    minimum_age = None

    maximum_age = None

    class Meta:
        form_classname = 'waf--field waf--html-field'
        icon = 'extraicons--paragraph'


