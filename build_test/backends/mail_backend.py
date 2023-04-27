from django.core.mail.backends.console import EmailBackend as DjangoConsoleBackend
from django.core.mail.backends.smtp import EmailBackend as DjangoEmailBackend


class DevEmailBackend:
    """
        Custom mail backend that uses a mail service on port 1025 but falls back to console if
        that service is not running.
        EMAIL_HOST = '127.0.0.1'
        EMAIL_PORT = 1025
    """
    def __init__(self, *args, **kwargs):
        self.email_backend = DjangoEmailBackend(*args, **kwargs)
        self.console_backend = DjangoConsoleBackend(*args, **kwargs)

    def send_messages(self, email_messages):
        try:
            return self.email_backend.send_messages(email_messages)
        except Exception:
            return self.console_backend.send_messages(email_messages)

    def open(self):
        """
        Stub method that allows the Wagtail backend to not fatal error
        when it's trying to send emails, such as moderation emails.
        """
        pass

    def close(self):
        """
        Stub method that allows the Wagtail backend to not fatal error
        when it's trying to send emails, such as moderation emails.
        """
        pass
