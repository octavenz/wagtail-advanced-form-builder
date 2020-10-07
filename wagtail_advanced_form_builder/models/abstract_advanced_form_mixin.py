import json

from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.rich_text import RichText

from wagtail_advanced_form_builder.blocks.fields import SingleLineFieldBlock
from wagtail_advanced_form_builder.forms import AdvancedFormBuilder
from .form_field import FormField

import wagtail_advanced_form_builder.constants as consts
from wagtail_advanced_form_builder.utils import clean_form_field_name
from ..blocks.fields.checkbox_field_block import CheckboxFieldBlock
from ..blocks.fields.checkboxes_field_block import CheckboxesFieldBlock
from ..blocks.fields.dropdown_field_block import DropdownFieldBlock
from ..blocks.fields.email_field_block import EmailFieldBlock
from ..blocks.fields.hidden_field_block import HiddenFieldBlock
from ..blocks.fields.html_field_block import HTMLFieldBlock
from ..blocks.fields.multi_line_field_block import MultiLineFieldBlock
from ..blocks.fields.multiselect_field_block import MultiSelectFieldBlock
from ..blocks.fields.number_field_block import NumberFieldBlock
from ..blocks.fields.radio_field_block import RadioFieldBlock
from ..blocks.fields.url_field_block import URLFieldBlock


def parse_condition_value(value):

    if value is False or value is None:
        return ''

    if value is True:
        return 'on'

    if isinstance(value, list):
        if len(value) == 0:
            return ''
        else:
            return ','.join(value)

    return value

def conditions_passed(condition_rule, condition_value, condition_field_value):

    condition_field_value = parse_condition_value(condition_field_value)

    if condition_rule == consts.FIELD_RULE_IS:
        if condition_field_value != condition_value:
            return False

    if condition_rule == consts.FIELD_RULE_IS_NOT:
        if condition_field_value == condition_value:
            return False

    if condition_rule == consts.FIELD_RULE_IS_BLANK:
        if condition_field_value != '':
            return False

    if condition_rule == consts.FIELD_RULE_IS_NOT_BLANK:
        if condition_field_value == '':
            return False

    if condition_rule == consts.FIELD_RULE_GREATER_THAN:
        try:
            condition_field_value = float(condition_field_value)
            condition_value = float(condition_value)
            if condition_field_value <= condition_value:
                return False
        except ValueError:
            pass

    if condition_rule == consts.FIELD_RULE_GREATER_THAN_OR_EQUAL:
        try:
            condition_field_value = float(condition_field_value)
            condition_value = float(condition_value)
            if condition_field_value < condition_value:
                return False
        except ValueError:
            pass

    if condition_rule == consts.FIELD_RULE_LESS_THAN:
        try:
            condition_field_value = float(condition_field_value)
            condition_value = float(condition_value)
            if condition_field_value >= condition_value:
                return False
        except ValueError:
            pass

    if condition_rule == consts.FIELD_RULE_LESS_THAN_OR_EQUAL:
        try:
            condition_field_value = float(condition_field_value)
            condition_value = float(condition_value)
            if condition_field_value > condition_value:
                return False
        except ValueError:
            pass

    if condition_rule == consts.FIELD_RULE_CONTAINS:
        if condition_value not in condition_field_value:
            return False

    if condition_rule == consts.FIELD_RULE_STARTS_WITH:
        if not condition_field_value.startsWith(condition_value):
            return False

    if condition_rule == consts.FIELD_RULE_ENDS_WITH:
        if not condition_field_value.endsWith(condition_value):
            return False

    return True


def clean_form(self):
    """
    Override the form builder form clean method to add validation to check for existing
    submissions
    :param self:
    :return:
    """

    for condition in self.conditional_rules:

        all_conditions_passed = True

        # Only check if the field is required
        field_required = condition['required']
        if field_required:
            action = condition['action']

            for cond in condition['conditions']:
                condition_rule = cond['rule']
                condition_value = cond['value']
                condition_field_value = self.cleaned_data.get(cond['field_name'], None)

                all_conditions_passed = conditions_passed(condition_rule, condition_value, condition_field_value)
                if not all_conditions_passed:
                    break

            if not all_conditions_passed and action == consts.FIELD_ACTION_SHOW:
                if condition['field_name'] in self._errors:
                    del self._errors[condition['field_name']]
            elif all_conditions_passed and action == consts.FIELD_ACTION_HIDE:
                if condition['field_name'] in self._errors:
                    del self._errors[condition['field_name']]

    return self.cleaned_data


class AbstractAdvancedFormMixin(models.Model):

    landing_page_template = 'wagtail_advanced_form_builder/page/form_complete.html'

    form_builder = AdvancedFormBuilder

    form_field = FormField

    form = StreamField(
        [
            (consts.FIELD_TYPE_SINGLE_LINE, SingleLineFieldBlock(label=_('Basic field'))),
            (consts.FIELD_TYPE_EMAIL, EmailFieldBlock(label=_('Email field'))),
            (consts.FIELD_TYPE_HTML, HTMLFieldBlock(label=_('HTML'))),
            (consts.FIELD_TYPE_DROPDOWN, DropdownFieldBlock(label=_('Dropdown field'))),
            (consts.FIELD_TYPE_RADIO, RadioFieldBlock(label=_('Radio field'))),
            (consts.FIELD_TYPE_CHECKBOXES, CheckboxesFieldBlock(label=_('Checkboxes field'))),
            (consts.FIELD_TYPE_CHECKBOX, CheckboxFieldBlock(label=_('Checkbox field'))),
            (consts.FIELD_TYPE_MULTI_SELECT, MultiSelectFieldBlock(label=_('Multiselect field'))),
            (consts.FIELD_TYPE_MULTI_LINE, MultiLineFieldBlock(label=_('Multiline field'))),
            (consts.FIELD_TYPE_URL, URLFieldBlock(label=_('URL field'))),
            (consts.FIELD_TYPE_HIDDEN, HiddenFieldBlock(label=_('Hidden field'))),
            (consts.FIELD_TYPE_NUMBER, NumberFieldBlock(label=_('Number field'))),
        ],
        default=None,
        null=True,
        blank=False,
        help_text=_('Add fields to the form')
    )

    thanks_page_title = models.CharField(
        max_length=150,
        default=None,
        null=True,
        blank=True,
        help_text=_('The title for the thanks page. Defaults to the normal page title if left blank.')
    )

    thanks_page_content = RichTextField(
        default=None,
        null=True,
        blank=False,
        help_text=_('Content to display on the form thank you page.')
    )

    submit_button_text = models.CharField(
        max_length=30,
        default=_('Submit'),
        help_text=_('The text to display on the form submission button'),
        blank=False,
    )

    use_browser_validation = models.BooleanField(
        blank=True,
        default=False,
        help_text=_('Tick this to use the in-built browser validation on fields')
    )

    content_panels = [
        StreamFieldPanel('form'),
        FieldPanel('submit_button_text'),
        MultiFieldPanel(
            [
                FieldPanel('thanks_page_title'),
                FieldPanel('thanks_page_content'),
            ],
            heading='Thanks page'
        ),
    ]

    settings_panels = [
        FieldPanel('use_browser_validation'),
    ]

    def get_template(self, request, *args, **kwargs):
        return 'wagtail_advanced_form_builder/page/form.html'

    def get_conditional_rules(self):
        """
        Retrieves the conditional rules that have been applied to this form within the CMS and exposes
        them to a dictionary which can be used to drive the front end form and to the form validator.
        :return: Dict
        """
        conditional_rules = []

        for field in self.form.get_prep_value():

            rules = field['value'].get('rules', None)
            if rules:
                field_id = field['value'].get('field_id', None)
                if field_id:
                    rules['field_name'] = field_id
                else:
                    rules['field_name'] = clean_form_field_name(field['value']['label'])
                rules['required'] = field['value'].get('required', False)
                rules['field_type'] = field.get('type', None)
                conditions = rules.get('conditions', None)
                if len(conditions):
                    for condition in conditions:
                        del(condition['id'])
                        del(condition['type'])
                        condition['field_name'] = clean_form_field_name(condition['value']['field_name'])
                        condition['rule'] = condition['value']['rule']
                        condition['value'] = condition['value'].get('value', None)

                    conditional_rules.append(rules)

        return conditional_rules

    def get_form(self, *args, **kwargs):

        """
        Overriden get_form method to allow for a custom validator on the form
        :param args:
        :param kwargs:
        :return:
        """

        # Call AbstractForm get_form method to retrieve form normally
        form = super().get_form(*args, **kwargs)

        # Dynamically override the clean method of the form builder form with a descriptor method
        form.clean = clean_form.__get__(form)

        # Attach anything else you need to the form in order to do your validation
        form.conditional_rules = self.get_conditional_rules()

        return form

    def get_data_fields(self):
        """
        Returns a list of tuples with (field_name, field_label).
        """
        data_fields = [
            ('submit_time', _('Submission date')),
        ]
        data_fields += [
            (field.clean_name, field.label)
            for field in self.get_form_fields(exclude_html=True)
        ]

        return data_fields

    def get_form_fields(self, exclude_html=False):
        """
        Get the form fields for this form by iterating over the streamfield block form fields and converting them
        into
        :param exclude_html:
        :return:
        """
        fields = []
        for field in self.form.get_prep_value():

            field_type = field['type']
            if exclude_html and field_type == consts.FIELD_TYPE_HTML:
                continue

            html_value = field['value'].get('html', None)
            if html_value:
                html_value = RichText(html_value)

            rule_action = ''
            rules = field['value'].get('rules', None)
            if rules:
                conditions = rules.get('conditions', None)
                if len(conditions):
                    rule_action = rules.get('action')

            form_field = self.form_field(
                field_type=field['type'],
                label=field['value']['label'],
                required=field['value'].get('required', False),
                choices=field['value'].get('choices', None),
                help_text=field['value'].get('help_text', None),
                default_value=field['value'].get('default_value', None),
                empty_label=field['value'].get('empty_label', None),
                max_length=field['value'].get('max_length', None),
                display_side_by_side=field['value'].get('display_side_by_side', False),
                display_checkbox_label=field['value'].get('display_checkbox_label', False),
                html_value=html_value,
                rule_action=rule_action,
            )

            fields.append(form_field)

        return fields

    def serve(self, request, *args, **kwargs):
        """
        Process the form submission. Overriding the abstract class method so we can redirect to the thanks page as opposed
        to just outputting it.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        template = self.get_template(request)

        if request.method == 'POST':

            form = self.get_form(request.POST, page=self, user=request.user)

            if form.is_valid():
                self.process_form_submission(form)
                return HttpResponseRedirect(self.url + '?thank=you')

        else:

            thanks = request.GET.get('thank', False)
            if thanks:
                form = None
                template = self.get_landing_page_template(request)
                if self.thanks_page_title:
                    self.title = self.thanks_page_title
            else:
                form = self.get_form(page=self, user=request.user)

        context = self.get_context(request)
        context['form'] = form
        if form:
            context['conditional_rules'] = json.dumps(form.conditional_rules)

        return render(
            request,
            template,
            context
        )

    class Meta:
        abstract = True
