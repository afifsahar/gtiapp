from django.apps import AppConfig


class CleaningConfig(AppConfig):
    name = 'cleaning'

    def ready(self):
        import cleaning.harians
        # import cleaning.tasks
