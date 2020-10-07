from wagtail_advanced_form_builder.blocks.base_static_block import BaseStaticBlock


class InlineFormBlock(BaseStaticBlock):
    """
    This block allows the user to position the form amongst other content on the page
    """
    class Meta:
        template = 'wagtail_advanced_form_builder/blocks/inline_form_block.html'
        icon = 'form'
        help_text = 'This will insert the form for this page into this position. ' \
                    'You can only add this block once on this page.'
        form_classname = ''
