from django.apps import AppConfig


class AccountapisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AccountApis'

    def ready(self):
    	from jobs import updater
    	updater.start()
