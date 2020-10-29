from django.forms import DateField
from django.forms.forms import DeclarativeFieldsMetaclass
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.widgets import AdminDateInput
from wagtail.contrib.forms.forms import SelectDateForm


class FormBuilderAdminSelectDateFormMeta(DeclarativeFieldsMetaclass):

    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        attr_meta = attrs.pop('Meta', None)
        meta = attr_meta or getattr(new_class, 'Meta', None)
        setattr(new_class, '_meta', meta)
        return new_class


class FormBuilderAdminSelectDateForm(SelectDateForm, metaclass=FormBuilderAdminSelectDateFormMeta):

    date_from = DateField(
        required=False,
        widget=AdminDateInput(attrs={'placeholder': 'Date from'})
    )
    date_to = DateField(
        required=False,
        widget=AdminDateInput(attrs={'placeholder': 'Date to'})
    )

    panels = [
        FieldPanel('date_from'),
        FieldPanel('date_to'),
    ]

    class Meta:
        fields = [
            'date_from',
            'date_to',
        ]
        exclude = []
