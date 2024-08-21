from wagtail import blocks

from wagtail_advanced_form_builder.forms.widgets.custom_select import CustomSelect
import wagtail_advanced_form_builder.constants as consts


class ConditionBlock(blocks.StructBlock):

    field_name = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text='The name of a field in the form'
    )

    rule = blocks.ChoiceBlock(
        choices=consts.FIELD_RULE_CHOICES,
        default=consts.FIELD_RULE_IS,
        widget=CustomSelect,
    )

    value = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=''
    )

    class Meta:
        icon = 'cog'
        form_classname = 'waf--rule-condition'
