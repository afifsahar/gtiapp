from django.apps import AppConfig
from .times import five_oclock


class CleaningConfig(AppConfig):
    name = 'cleaning'

    # def ready(self):
    #     import cleaning.functionRun
