from django.utils.translation import ugettext_lazy as _

FIELD_TYPE_SINGLE_LINE = 'singleline'
FIELD_TYPE_MULTI_LINE = 'multiline'
FIELD_TYPE_EMAIL = 'email'
FIELD_TYPE_NUMBER = 'number'
FIELD_TYPE_URL = 'url'
FIELD_TYPE_CHECKBOX = 'checkbox'
FIELD_TYPE_CHECKBOXES = 'checkboxes'
FIELD_TYPE_DROPDOWN = 'dropdown'
FIELD_TYPE_MULTI_SELECT = 'multiselect'
FIELD_TYPE_RADIO = 'radio'
FIELD_TYPE_DATE = 'date'
FIELD_TYPE_HIDDEN = 'hidden'
FIELD_TYPE_HTML = 'html'
FIELD_TYPE_CURRENCY = 'currency'
FIELD_TYPE_SIMPLE_DATE = 'simpledate'
FIELD_TYPE_PHONE = 'phone'

FIELD_RULE_IS = 'is'
FIELD_RULE_IS_NOT = 'is_not'
FIELD_RULE_GREATER_THAN = 'greater_than'
FIELD_RULE_GREATER_THAN_OR_EQUAL = 'greater_than_equal'
FIELD_RULE_LESS_THAN = 'less_than'
FIELD_RULE_LESS_THAN_OR_EQUAL = 'less_than_equal'
FIELD_RULE_CONTAINS = 'contains'
FIELD_RULE_STARTS_WITH = 'starts-with'
FIELD_RULE_ENDS_WITH = 'ends-with'
FIELD_RULE_IS_BLANK = 'is_blank'
FIELD_RULE_IS_NOT_BLANK = 'is_not_blank'

FIELD_RULE_CHOICES = (
    (FIELD_RULE_IS, _('Is equal to')),
    (FIELD_RULE_IS_NOT, _('Is not equal to')),
    (FIELD_RULE_GREATER_THAN, _('Greater than')),
    (FIELD_RULE_GREATER_THAN_OR_EQUAL, _('Greater than or equal to')),
    (FIELD_RULE_LESS_THAN, _('Less than')),
    (FIELD_RULE_LESS_THAN_OR_EQUAL, _('Less than or equal to')),
    (FIELD_RULE_CONTAINS, _('Contains')),
    (FIELD_RULE_STARTS_WITH, _('Starts with')),
    (FIELD_RULE_ENDS_WITH, _('Ends with')),
)

FIELD_RULE_CHOICES_BLANK = (
    (FIELD_RULE_IS_BLANK, _('Is blank')),
    (FIELD_RULE_IS_NOT_BLANK, _('Is not blank')),
)

FIELD_ACTION_SHOW = 'show'
FIELD_ACTION_HIDE = 'hide'
FIELD_ACTION_CHOICES = (
    (FIELD_ACTION_SHOW, _('Show')),
    (FIELD_ACTION_HIDE, _('Hide')),
)
