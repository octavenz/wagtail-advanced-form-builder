import datetime

from django.forms import DateInput
from django.utils import formats
from django.conf import settings

from wagtail_advanced_form_builder.utils import to_waf_datetimepicker_format


class DatePickerWidget(DateInput):

    template_name = 'wagtail_advanced_form_builder/widgets/datepicker_widget.html'

    @property
    def date_format(self):
        return getattr(settings, 'WAGTAIL_DATE_FORMAT', self.format or formats.get_format(self.format_key)[0])

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        # Reformat the chosen Django date string into something the frontend datepicker can use.
        attrs['data-waf-date-format'] = to_waf_datetimepicker_format(self.date_format)
        return attrs

    def format_value(self, value):
        # From what I can ascertain from examining the Django models.DateField is that DateFields are always stored
        # as YYYY-MM-DD format in the db. So we have a string here in that format always in theory. So convert that to
        # a date and then fling it through the localize_input method to get it out how we want it for display.
        if isinstance(value, datetime.date):
            date_value = value.strftime(self.date_format)
        else:
            date_value = datetime.datetime.strptime(value, '%Y-%m-%d').date()
        return formats.localize_input(date_value, self.date_format)

