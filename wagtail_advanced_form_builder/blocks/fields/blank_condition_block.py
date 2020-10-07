import wagtail_advanced_form_builder.constants as consts

from wagtail.core import blocks

from .condition_block import ConditionBlock


class BlankConditionBlock(ConditionBlock):

    rule = blocks.ChoiceBlock(
        choices=consts.FIELD_RULE_CHOICES_BLANK,
        default=consts.FIELD_RULE_IS_BLANK,
    )

    value = None

    class Meta:
        icon = 'cog'

