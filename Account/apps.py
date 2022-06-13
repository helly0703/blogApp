from django.apps import AppConfig


class UsersConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'Account'

    def ready(self):
        import Account.signals