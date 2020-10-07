from django.utils.text import slugify
from unidecode import unidecode


def clean_form_field_name(label):
    # unidecode will return an ascii string while slugify wants a
    # unicode string on the other hand, slugify returns a safe-string
    # which will be converted to a normal str
    return str(slugify(str(unidecode(label))))
