from wagtail import blocks

from .condition_block import ConditionBlock
from ...forms.widgets.custom_select import CustomSelect
import wagtail_advanced_form_builder.constants as consts


class BlankConditionBlock(ConditionBlock):

    rule = blocks.ChoiceBlock(
        choices=consts.FIELD_RULE_CHOICES_BLANK,
        default=consts.FIELD_RULE_IS_BLANK,
        widget=CustomSelect,
    )

    value = None

    class Meta:
        icon = 'cog'
