from wagtail.contrib.forms.models import AbstractForm

from .abstract_advanced_form_mixin import AbstractAdvancedFormMixin


class AbstractAdvancedForm(AbstractAdvancedFormMixin, AbstractForm):

    settings_panels = AbstractAdvancedFormMixin.settings_panels

    class Meta:
        abstract = True
