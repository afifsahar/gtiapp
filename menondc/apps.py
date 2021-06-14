from django.apps import AppConfig
from .times import five_oclock


class MenondcConfig(AppConfig):
    name = 'menondc'

    # def ready(self):
    #     import menondc.functionRun
