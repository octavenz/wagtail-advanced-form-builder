from .date_field_block import DateFieldBlock


class DatePickerFieldBlock(DateFieldBlock):
    class Meta:
        form_classname = 'waf--field'
        icon = 'date'
