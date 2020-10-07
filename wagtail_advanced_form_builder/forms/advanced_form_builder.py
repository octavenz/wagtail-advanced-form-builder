from django import forms
from wagtail.contrib.forms.forms import FormBuilder

from wagtail_advanced_form_builder.forms.widgets.checkbox_input_widget import CheckboxInput
from wagtail_advanced_form_builder.forms.widgets.html_output_widget import HTMLOutputWidget
from wagtail_advanced_form_builder.forms.widgets.side_by_side_radio_select_widget import SideBySideRadioSelectWidget


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


