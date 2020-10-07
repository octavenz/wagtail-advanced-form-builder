from django.forms import RadioSelect


class SideBySideRadioSelectWidget(RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_side_by_side = True
