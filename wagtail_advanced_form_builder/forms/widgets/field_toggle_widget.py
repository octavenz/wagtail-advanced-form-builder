from django.forms import CheckboxInput, Media


class FieldToggleInput(CheckboxInput):
    template_name = "wagtail_advanced_form_builder/widgets/field_toggle_widget.html"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["label"] = context["widget"]["attrs"]["data-label"]
        context["widget"]["toggled_label"] = context["widget"]["attrs"][
            "data-toggled-label"
        ]
        context["widget"]["id_for_label"] = context["widget"]["attrs"]["id"]
        return context

    @property
    def media(self):
        css = {}
        js = ["wagtail_advanced_form_builder/js/field-toggle-widget.js"]
        return Media(css=css, js=js)
