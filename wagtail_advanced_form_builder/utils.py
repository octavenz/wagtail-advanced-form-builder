# anyascii is a Wagtail dependency
import re
from anyascii import anyascii
from django.utils.text import slugify
from wagtail.rich_text import expand_db_html


def clean_form_field_name(label):
    # anyascii will return an ascii string while slugify wants a
    # unicode string on the other hand, slugify returns a safe-string
    # which will be converted to a normal str
    return str(slugify(str(anyascii(label))))


def modified_html(value):
    external_link_pattern = r'<a href="(http[s]?://[^"]*)">([^<]*)</a>'
    hyperlink_replacement = r'<a href="\1" rel="noopener noreferrer" target="_blank">\2</a>'
    # Get the source the value
    source = value.source
    # Use expand_db_html to extract html data
    expanded_html = expand_db_html(source)
    # Replace all external links with ones that open in a new tab
    modified_html = re.sub(external_link_pattern, hyperlink_replacement, expanded_html)
    return modified_html
