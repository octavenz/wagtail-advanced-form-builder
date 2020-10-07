from django.forms import  Widget


class HTMLOutputWidget(Widget):

    html_value = None

    template_name = "wagtail_advanced_form_builder/widgets/html_output_widget.html"

    def __init__(self, html_value=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.html_value = html_value

    def get_context(self, *args, **kwargs):

        context = super().get_context(*args, **kwargs)

        context['widget'].update({
            'html_value': self.html_value,
        })

        return context
