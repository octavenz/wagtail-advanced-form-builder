import wagtail_advanced_form_builder.constants as consts
from pydantic import Field
from wagtail_advanced_form_builder.models import FormPage, EmailFormPage

from wagtail_advanced_form_builder.utils import modified_html
from ninja import Schema
from typing import Literal, List, Optional, Union, Dict, Any, Type, Annotated


# Placeholder for conditional ruleset
class FormRuleConditionSchema(Schema):
    field_name: str
    rule: Literal[
        'is',
        'is_not',
        'greater_than',
        'greater_than_equal',
        'less_than',
        'less_than_equal',
        'contains',
        'starts-with',
        'ends-with',
    ]
    value: str


class FormRuleBlankConditionSchema(Schema):
    field_name: str
    rule: Literal[
        'is_blank',
        'is_not_blank'
    ]


class FormRuleSchema(Schema):
    action: Literal["show", "hide"] = consts.FIELD_ACTION_SHOW
    conditions: Optional[
        List[
            Union[
                FormRuleConditionSchema,
                FormRuleBlankConditionSchema
            ]
        ]
    ] = []

    class Config:
        extra = "ignore"


class BaseFieldSchema(Schema):
    id: int
    type: str  # This is our discriminator field
    name: str
    label: Optional[str] = None
    required: Optional[bool] = False
    help_text: Optional[str] = None
    rules: Optional[FormRuleSchema] = None


class SingleLineSchema(BaseFieldSchema):
    type: Literal["singleline"] = consts.FIELD_TYPE_SINGLE_LINE
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class MultiLineSchema(BaseFieldSchema):
    type: Literal["multiline"] = consts.FIELD_TYPE_MULTI_LINE
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class HTMLSchema(BaseFieldSchema):
    type: Literal["html"] = consts.FIELD_TYPE_HTML
    html: str


class DropdownSchema(BaseFieldSchema):
    type: Literal["dropdown"] = consts.FIELD_TYPE_DROPDOWN
    choices: Optional[List[str]] = []
    empty_label: Optional[str] = None
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class CheckboxSchema(BaseFieldSchema):
    type: Literal["checkbox"] = consts.FIELD_TYPE_CHECKBOX
    display_checkbox_label: Optional[bool] = False
    help_text: Optional[str] = None


class CheckboxesSchema(BaseFieldSchema):
    type: Literal["checkboxes"] = consts.FIELD_TYPE_CHECKBOXES
    choices: Optional[List[str]] = []
    display_side_by_side: Optional[bool] = None
    default_value: Optional[List[str]] = []


class MultiSelectSchema(BaseFieldSchema):
    type: Literal["multiselect"] = consts.FIELD_TYPE_MULTI_SELECT
    choices: Optional[List[str]] = []
    default_value: Optional[str] = None


class RadioSchema(BaseFieldSchema):
    type: Literal["radio"] = consts.FIELD_TYPE_RADIO
    choices: Optional[List[str]] = []
    display_side_by_side: Optional[bool] = None
    default_value: Optional[str] = None


class UrlSchema(BaseFieldSchema):
    type: Literal["url"] = consts.FIELD_TYPE_URL
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class NumberSchema(BaseFieldSchema):
    type: Literal["number"] = consts.FIELD_TYPE_NUMBER
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class EmailSchema(BaseFieldSchema):
    type: Literal["email"] = consts.FIELD_TYPE_EMAIL
    max_length: Optional[int] = None
    default_value: Optional[str] = None


class HiddenSchema(BaseFieldSchema):
    type: Literal["hidden"] = consts.FIELD_TYPE_HIDDEN
    default_value: str  # Required for hidden fields


# Corrected mapping with all field types
FORM_FIELDS_MAPPING = {
    consts.FIELD_TYPE_SINGLE_LINE: SingleLineSchema,
    consts.FIELD_TYPE_MULTI_LINE: MultiLineSchema,
    consts.FIELD_TYPE_HTML: HTMLSchema,
    consts.FIELD_TYPE_DROPDOWN: DropdownSchema,
    consts.FIELD_TYPE_CHECKBOX: CheckboxSchema,
    consts.FIELD_TYPE_CHECKBOXES: CheckboxesSchema,
    consts.FIELD_TYPE_MULTI_SELECT: MultiSelectSchema,
    consts.FIELD_TYPE_RADIO: RadioSchema,
    consts.FIELD_TYPE_URL: UrlSchema,
    consts.FIELD_TYPE_NUMBER: NumberSchema,
    consts.FIELD_TYPE_EMAIL: EmailSchema,
    consts.FIELD_TYPE_HIDDEN: HiddenSchema
}

# Form fields union
FormFieldUnion = Annotated[
    Union[
        SingleLineSchema,
        MultiLineSchema,
        HTMLSchema,
        DropdownSchema,
        CheckboxSchema,
        CheckboxesSchema,
        MultiSelectSchema,
        RadioSchema,
        UrlSchema,
        NumberSchema,
        EmailSchema,
        HiddenSchema
    ],
    Field(discriminator='type')
]


class JSONResponse(Schema):
    message: Optional[str] = None
    details: Optional[dict] = {}


class FormPostSchema(Schema):
    form_fields: Dict[str, Any]
    path: str
    # site: @TODO Handling multisite or default to site in Wagtail settings


class FormFieldSubmission(Schema):
    id: int
    name: str
    type: Optional[str]
    value: Any = None
    required: Optional[bool] = False


class ThanksPageSchema(Schema):
    thanks_page_title: Optional[str] = None
    thanks_page_content: str


class BaseFormPageSchema(Schema):
    class Config:
        model = FormPage
        model_fields = "__all__"
        custom_fields = [
            ('fields', List[FormFieldUnion], []),
            ('form_submission_schema', Dict, {}),
        ]
        populate_by_name = True

    id: int
    title: str
    thanks_page_title: Optional[str] = None
    thanks_page_content: str
    submit_button_text: str
    search_description: Optional[str] = None
    seo_title: Optional[str] = None
    show_in_menus: bool = False
    use_browser_validation: bool = False
    fields: List[FormFieldUnion]
    type: str

    @staticmethod
    def resolve_fields(obj):
        # This method is called when serialized or deserializing
        # So we need to handle when a dictionary is passed into this as obj
        if isinstance(obj, dict):
            return obj['fields']

        # This method is called when serialized/deserializing/validating
        # So we need to handle when FormPageSchema is passed
        if isinstance(obj, BaseFormPageSchema):
            return obj.fields

        # This method is called when serialized/deserializing/validating
        # so we need to handle when a Django Model instance is passed in
        form_fields = []
        clean_name_lookup = {
            form_field.label: form_field.clean_name for form_field in obj.get_form_fields()
        }

        for idx, block in enumerate(obj.form):
            try:
                block_schema = FORM_FIELDS_MAPPING.get(block.block_type)
                if not block_schema:
                    print(f"No schema found for block type: {block.block_type}")
                    continue
                block_data = {'type': block.block_type, 'id': idx}

                # Extract block data from the value
                for key, value in block.value.items():
                    if isinstance(value, (str, int, float, bool, type(None))):
                        block_data[key] = value
                        # get clean name from form field
                        if key == 'label':
                            block_data['name'] = clean_name_lookup[value]

                    elif key == 'rules' and (isinstance(value, dict) or hasattr(value, 'items')):
                        # Create a dictionary for rules
                        rules_data = {'action': value.get('action')}
                        conditions_stream = value.get('conditions')

                        # Process conditions if they exist
                        if conditions_stream:
                            conditions = []
                            for condition_block in conditions_stream:
                                condition_data = {}
                                # Extract condition properties using dictionary access
                                condition_value = condition_block.value
                                if hasattr(condition_value, 'get'):
                                    condition_data['field_name'] = condition_value.get('field_name')
                                    condition_data['rule'] = condition_value.get('rule')
                                    condition_data['value'] = condition_value.get('value')
                                else:
                                    # If condition_value is a real dictionary
                                    condition_data = {k: v for k, v in condition_value.items()}
                                conditions.append(condition_data)

                            rules_data['conditions'] = conditions

                        block_data[key] = rules_data
                    elif key == 'html' and hasattr(value, 'source'):
                        block_data[key] = modified_html(value)
                    elif hasattr(value, 'raw_data') and isinstance(value.raw_data, list):
                        # Handle ListValue objects using their raw_data attribute
                        block_data[key] = value.raw_data
                    elif hasattr(value, '__iter__') and not isinstance(value, (str, dict)):
                        # Try to convert to a list of simple values
                        block_data[key] = [item for item in value]
                    elif isinstance(value, dict):
                        # For dictionaries, keep only serializable values
                        block_data[key] = {
                            k: v for k, v in value.items()
                            if isinstance(v, (str, int, float, bool, list, dict, type(None)))
                        }
                    else:
                        # Try to get a string representation for other types
                        block_data[key] = str(value)

                instance = block_schema(**block_data)
                form_fields.append(instance)
            except Exception as e:
                print(f"Error processing field: {e}")
        return form_fields


class FormPageSchema(BaseFormPageSchema):
    type: Literal["form_page"] = consts.FORM_PAGE

    class Config:
        model = FormPage


class EmailFormPageSchema(BaseFormPageSchema):
    type: Literal["email_form_page"] = consts.EMAIL_FORM_PAGE
    from_address: str
    to_address: str
    subject: str

    class Config:
        model = EmailFormPage


FormPageUnion = Annotated[
    Union[FormPageSchema, EmailFormPageSchema],
    Field(discriminator='type')
]
