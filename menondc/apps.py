from django.apps import AppConfig


class MenondcConfig(AppConfig):
    name = 'menondc'

    def ready(self):
        import menondc.harians
        import menondc.tasks

