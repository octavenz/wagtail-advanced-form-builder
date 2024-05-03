from wagtail import blocks

from .checkbox_field_block import CheckboxFieldBlock


class FieldToggleBlock(CheckboxFieldBlock):
    name = blocks.CharBlock(
        max_length=255, required=False, help_text="The field name to be used in the code"
    )
    toggled_label = blocks.CharBlock(
        max_length=255, required=False, help_text="The label to display when toggled"
    )
