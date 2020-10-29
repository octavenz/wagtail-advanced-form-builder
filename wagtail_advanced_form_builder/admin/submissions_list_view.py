import datetime

from wagtail.contrib.forms.views import SubmissionsListView

from wagtail_advanced_form_builder.admin.forms.admin_select_date_form import FormBuilderAdminSelectDateForm


class FormBuilderSubmissionsListView(SubmissionsListView):

    def get_filtering(self):
        """ Return filtering as a dict for submissions queryset """
        self.select_date_form = FormBuilderAdminSelectDateForm(self.request.GET)
        result = dict()
        if self.select_date_form.is_valid():
            date_from = self.select_date_form.cleaned_data.get('date_from')
            date_to = self.select_date_form.cleaned_data.get('date_to')
            if date_to:
                # careful: date_to must be increased by 1 day
                # as submit_time is a time so will always be greater
                date_to += datetime.timedelta(days=1)
                if date_from:
                    result['submit_time__range'] = [date_from, date_to]
                else:
                    result['submit_time__lte'] = date_to
            elif date_from:
                result['submit_time__gte'] = date_from
        return result
