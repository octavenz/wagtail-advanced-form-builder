# anyascii is a Wagtail dependency
from anyascii import anyascii

from django.utils.text import slugify


def clean_form_field_name(label):
    # anyascii will return an ascii string while slugify wants a
    # unicode string on the other hand, slugify returns a safe-string
    # which will be converted to a normal str
    return str(slugify(str(anyascii(label))))
