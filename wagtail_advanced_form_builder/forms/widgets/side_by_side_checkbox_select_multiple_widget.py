from django.forms import CheckboxSelectMultiple


class SideBySideCheckboxSelectWidget(CheckboxSelectMultiple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_side_by_side = True
