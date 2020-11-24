# import datetime
# from datetime import date, timedelta
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import *

# day_test = date.today()-datetime.timedelta(days=5)

# if not mendc_day.objects.filter(hariIni=date.today()):
#     mendc_day(hariIni=date.today()).save()

# for subareas in mendc_subarea.objects.all():
#     defaults = mendc_default.objects.filter(defaultSubarea=subareas)
#     harians = mendc_daily.objects.filter(
#         dailySubarea=subareas, hariIni=date.today())
#     if not defaults:
#         defaults = mendc_default(defaultSubarea=subareas)
#         defaults.save()
#     if not harians:
#         harians = mendc_daily(dailySubarea=subareas, hariIni=date.today())
#         harians.save()

# for subareas in mendc_subarea.objects.all():
#     defaults = mendc_default.objects.get(defaultSubarea=subareas)
#     harians = mendc_daily.objects.filter(
#         dailySubarea=subareas, hariIni=date.today())
#     for harian in harians:
#         harian.hariIni = datetime(
#             date.today().year, date.today().month, date.today().day)  # time 00:00:00
#         harian.kondisi = defaults.defaultKondisi
#         harian.keterangan = defaults.defaultKeterangan
#         harian.hasilTemuan = defaults.defaultHasilTemuan
#         harian.save()

import datetime
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=mendc_subarea)
def create_daily(sender, instance, created, **kwargs):
    if created:
        harians = mendc_daily.objects.create(
            dailySubarea=instance, hariIni=date.today())
        defaults = mendc_default.objects.create(
            defaultSubarea=instance, hariIni=date.today())
        for (harian, default) in zip(harians, defaults):
            harian.hariIni = datetime(
                date.today().year, date.today().month, date.today().day)  # time 00:00:00
            harian.kondisi = default.defaultKondisi
            harian.keterangan = default.defaultKeterangan
            harian.hasilTemuan = default.defaultHasilTemuan
            harian.save()


@receiver(post_save, sender=mendc_subarea)
def save_daily(sender, instance, **kwargs):
    instance.dailySubarea.save()
    instance.defaultSubarea.save()


@receiver(post_save, sender=mendc_subarea)
def update_daily(sender, instance, created, **kwargs):
    if created == False:
        instance.dailySubarea.save()
        instance.defaultSubarea.save()