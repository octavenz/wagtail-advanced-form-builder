from django import template

register = template.Library()


@register.filter('fieldtype')
def fieldtype(field):
    return field.field.widget.__class__.__name__


@register.inclusion_tag('wagtail_advanced_form_builder/tags/form_field.html', takes_context=True)
def form_field(context, field):
    return {
        'field': field,
    }


@register.simple_tag
def wrap_form_builder_field(field):
    try:
        field_type = fieldtype(field)
        field_class = ''
        attrs = field.field.widget.attrs
        attrs['class'] = field_class
        field.field.widget.attrs = attrs

    except Exception as e:
        return field

    return field
