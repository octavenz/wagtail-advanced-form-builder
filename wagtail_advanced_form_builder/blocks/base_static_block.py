from django.template.loader import render_to_string
from wagtail.core import blocks


class BaseStaticBlock(blocks.StaticBlock):
    """
    This is used instead of blocks.StaticBlock to control markup in admin and apply styling
    """
    def render_form(self, value, prefix='', errors=None):
        return render_to_string('wagtail_advanced_form_builder/admin/blocks/base_static_block.html', {
            'name': self.name,
            'text': self.meta.help_text,
            'classes': self.meta.form_classname,
        })
