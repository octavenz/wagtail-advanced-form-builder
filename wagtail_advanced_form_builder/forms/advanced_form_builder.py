import datetime

from django import forms
from django.conf import settings
from django.utils import formats

from wagtail.contrib.forms.forms import FormBuilder

from wagtail_advanced_form_builder.forms.widgets.datepicker_widget import DatePickerWidget
from wagtail_advanced_form_builder.forms.widgets.checkbox_input_widget import CheckboxInput
from wagtail_advanced_form_builder.forms.widgets.html_output_widget import HTMLOutputWidget
from wagtail_advanced_form_builder.forms.widgets.side_by_side_radio_select_widget import SideBySideRadioSelectWidget
from wagtail_advanced_form_builder.utils import get_datepicker_date_format


class AdvancedFormBuilder(FormBuilder):

    def create_singleline_field(self, field, options):
        if field.max_length:
            options['max_length'] = field.max_length
        else:
            options['max_length'] = 255
        return forms.CharField(**options)

    def create_email_field(self, field, options):
        if field.max_length:
            options['max_length'] = field.max_length
        return forms.EmailField(**options)

    def create_url_field(self, field, options):
        if field.max_length:
            options['max_length'] = field.max_length
        return forms.URLField(**options)

    def create_html_field(self, field, options):
        options['widget'] = HTMLOutputWidget(
            html_value=field.html_value,
        )
        return forms.Field(**options)

    def create_dropdown_field(self, field, options):
        options['choices'] = list(map(
            lambda x: (x.strip(), x.strip()),
            field.choices
        ))
        if field.empty_label:
            options['choices'] = [('', field.empty_label)] + options['choices']

        return forms.ChoiceField(**options)

    def create_checkboxes_field(self, field, options):
        options['choices'] = list(map(
            lambda x: (x.strip(), x.strip()),
            field.choices
        ))
        options['initial'] = list(map(
            lambda x: (x.strip(), x.strip()),
            field.default_value
        ))
        return forms.MultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, **options
        )

    def create_checkbox_field(self, field, options):
        options['widget'] = CheckboxInput(
            display_checkbox_label=field.display_checkbox_label
        )
        return forms.BooleanField(**options)


    def create_radio_field(self, field, options):

        options['choices'] = list(map(
            lambda x: (x.strip(), x.strip()),
            field.choices
        ))

        if field.display_side_by_side:
            return forms.ChoiceField(widget=SideBySideRadioSelectWidget, **options)
        else:
            return forms.ChoiceField(widget=forms.RadioSelect, **options)


    def create_multiselect_field(self, field, options):
        options['choices'] = list(map(
            lambda x: (x.strip(), x.strip()),
            field.choices
        ))
        return forms.MultipleChoiceField(**options)

    def create_datepicker_field(self, field, options):

        widget_attrs = {
            'data-waf-datepicker': True,
        }

        if field.maximum_date:
            if isinstance(field.maximum_date, datetime.date):
                max_date = field.maximum_date.strftime(get_datepicker_date_format())
            else:
                max_date = datetime.datetime.strptime(field.maximum_date, '%Y-%m-%d').date()
            widget_attrs['data-waf-datepicker-max-date'] = formats.localize_input(max_date, get_datepicker_date_format())

        if field.minimum_date:
            if isinstance(field.minimum_date, datetime.date):
                min_date = field.minimum_date.strftime(get_datepicker_date_format())
            else:
                min_date = datetime.datetime.strptime(field.minimum_date, '%Y-%m-%d').date()
            widget_attrs['data-waf-datepicker-min-date'] = formats.localize_input(min_date, get_datepicker_date_format())

        options['widget'] = DatePickerWidget(
            attrs=widget_attrs,
        )
        return forms.DateField(
            input_formats=[
                get_datepicker_date_format(),
                '%Y-%m-%d',
            ],
            **options
        )


