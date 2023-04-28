from django.apps import AppConfig


class WagtailAdvancedFormBuilderConfig(AppConfig):
    name = 'wagtail_advanced_form_builder'
    verbose_name = 'Wagtail advanced form builder'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        pass

