from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import MultiFieldPanel, FieldRowPanel, FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm
from .abstract_advanced_form_mixin import AbstractAdvancedFormMixin
from .email_form_field import EmailFormField

class AbstractAdvancedEmailForm(AbstractAdvancedFormMixin, AbstractEmailForm):

    form_field = EmailFormField

    content_panels = AbstractAdvancedFormMixin.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6')
            ]),
            FieldPanel('subject'),
        ], _('Email')),
    ]

    settings_panels = AbstractAdvancedFormMixin.settings_panels

    class Meta:
        abstract = True
