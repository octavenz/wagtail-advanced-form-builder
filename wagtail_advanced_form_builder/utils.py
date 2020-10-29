from django.utils import formats
from django.utils.text import slugify
from django.conf import settings
from unidecode import unidecode
from datetime import datetime



def clean_form_field_name(label):
    # unidecode will return an ascii string while slugify wants a
    # unicode string on the other hand, slugify returns a safe-string
    # which will be converted to a normal str
    return str(slugify(str(unidecode(label))))

def to_waf_datetimepicker_format(python_format_string):
    """
    Given a python datetime format string, attempts to convert it to
    the nearest Javascript datetime format string possible.
    """
    python_to_javascript = {
        "%d": "dd",
        "%j": "d",
        "%l": "DD",
        "%n": "m",
        "%m": "mm",
        "%F": "MM",
        "%y": "yy",
        "%Y": "yyyy",
    }

    javascript_format_string = python_format_string
    for py, js in python_to_javascript.items():
        javascript_format_string = javascript_format_string.replace(py, js)

    return javascript_format_string

def parse_date_string_to_date(date_string, date_format):
    return datetime.strptime(date_string, date_format).date()

def get_datepicker_date_format():
    return getattr(settings, 'WAGTAIL_DATE_FORMAT', formats.get_format('DATE_INPUT_FORMATS')[0])
