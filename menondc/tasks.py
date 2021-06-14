# from __future__ import absolute_import, unicode_literals
# from django.core.management import call_command
# import sys

# from celery import shared_task

import datetime
from datetime import date, timedelta
from .models import *


# @shared_task
def create_daily():
    if not mendc_day.objects.filter(hariIni=date.today()):
        mendc_day(hariIni=date.today()).save()

    for subareas in mendc_subarea.objects.all():
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = mendc_default(defaultSubarea=subareas)
            defaults.save()
        if not harians:
            harians = mendc_daily(dailySubarea=subareas, hariIni=date.today())
            harians.save()
        for default in defaults:
            harians.hariIni = datetime(
                date.today().year, date.today().month, date.today().day)  # time 00:00:00
            harians.kondisi = default.defaultKondisi
            harians.keterangan = default.defaultKeterangan
            harians.hasilTemuan = default.defaultHasilTemuan
    # for subareas in mendc_subarea.objects.all():
    #     defaults = mendc_default.objects.filter(defaultSubarea=subareas)
    #     harians = mendc_daily.objects.filter(
    #         dailySubarea=subareas, hariIni=date.today())
        # for (harian, default) in zip(harians, defaults):
        #     harian.hariIni = datetime(
        #         date.today().year, date.today().month, date.today().day)  # time 00:00:00
        #     harian.kondisi = default.defaultKondisi
        #     harian.keterangan = default.defaultKeterangan
        #     harian.hasilTemuan = default.defaultHasilTemuan
        #     harian.save()


# @shared_task
# def bkup():
#     sys.stdout = open('menondc_db.json', 'w')
#     call_command('dumpdata', 'menondc')
