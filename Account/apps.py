from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'Account'

    def ready(self):
        import Account.signals