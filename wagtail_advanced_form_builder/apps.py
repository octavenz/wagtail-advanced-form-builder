from django.apps import AppConfig
from django.conf import settings


class WagtailAdvancedFormBuilderConfig(AppConfig):
    name = 'wagtail_advanced_form_builder'
    verbose_name = 'Wagtail advanced form builder'
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        # Handling Django recaptcha required RECAPTCHA_PUBLIC_KEY & RECAPTCHA_PRIVATE_KEY
        # as this will be need to set in project django settings
        if not hasattr(settings, 'SILENCED_SYSTEM_CHECKS'):
            setattr(settings, 'SILENCED_SYSTEM_CHECKS', ['django_recaptcha.recaptcha_test_key_error'])
        else:
            if 'django_recaptcha.recaptcha_test_key_error' not in settings.SILENCED_SYSTEM_CHECKS:
                settings.SILENCED_SYSTEM_CHECKS.append('django_recaptcha.recaptcha_test_key_error')

