import datetime
from datetime import date, timedelta
from cleaning.models import *

def cln_autos():
    if not cln_day.objects.filter(hariIni=date.today()):
        cln_day(hariIni=date.today()).save()

    for subareas in cln_subarea.objects.all():
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

    for subareas in cln_subarea.objects.all():
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        for default in defaults:
            harians.hariIni = datetime(
                date.today().year, date.today().month, date.today().day)  # time 00:00:00
            harians.kondisi = default.defaultKondisi
            harians.keterangan = default.defaultKeterangan
            harians.hasilTemuan = default.defaultHasilTemuan