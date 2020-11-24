# from __future__ import absolute_import, unicode_literals
# from django.core.management import call_command
# import sys

# from celery import shared_task

import datetime
from datetime import date, timedelta
from .models import *


# @shared_task
def create_daily():
    if not cln_day.objects.filter(hariIni=date.today()):
        cln_day(hariIni=date.today()).save()

    for subareas in cln_subarea.objects.all():
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
            # defaults.save()
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())
            # harians.save()
    # for subareas in cln_subarea.objects.all():
    #     defaults = cln_default.objects.filter(defaultSubarea=subareas)
    #     harians = cln_daily.objects.filter(
    #         dailySubarea=subareas, hariIni=date.today())
        for default in defaults:
            harians.hariIni = datetime(
                date.today().year, date.today().month, date.today().day)  # time 00:00:00
            harians.kondisi = default.defaultKondisi
            harians.keterangan = default.defaultKeterangan
            harians.hasilTemuan = default.defaultHasilTemuan
            # harians.save()


# @shared_task
# def bkup():
#     sys.stdout = open('cleaning_db.json', 'w')
#     call_command('dumpdata', 'cleaning')
