import wagtail_advanced_form_builder.constants as consts

from wagtail import blocks

from .condition_block import ConditionBlock
from .blank_condition_block import BlankConditionBlock
from ...forms.widgets.custom_select import CustomSelect


class ConditionalBlock(blocks.StructBlock):

    action = blocks.ChoiceBlock(
        choices=consts.FIELD_ACTION_CHOICES,
        default=consts.FIELD_ACTION_SHOW,
        help_text='What conditional action would you like to perform on this field?',
        required=True,
        widget=CustomSelect,
    )

    conditions = blocks.StreamBlock(
        [
            ('condition', ConditionBlock()),
            ('blank_condition', BlankConditionBlock()),
        ],
        required=False,
    )

    class Meta:
        icon = 'cog'
        form_classname = 'waf--form-rules waf--field-content'
