import wagtail_advanced_form_builder.constants as consts

from wagtail.core import blocks

from .condition_block import ConditionBlock
from .blank_condition_block import BlankConditionBlock


class ConditionalBlock(blocks.StructBlock):

    action = blocks.ChoiceBlock(
        choices=consts.FIELD_ACTION_CHOICES,
        default=consts.FIELD_ACTION_SHOW,
        help_text='What conditional action would you like to perform on this field?',
        required=True,
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
