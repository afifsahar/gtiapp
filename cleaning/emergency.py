import datetime
from datetime import date, timedelta
from cleaning.models import *

emerg_date = date(2020, 12, 22)


# def cln_when_day_fail():
if not cln_day.objects.filter(hariIni=emerg_date):
    cln_day(hariIni=emerg_date).save()

for subareas in cln_subarea.objects.all():
    defaults = cln_default.objects.filter(defaultSubarea=subareas)
    harians = cln_daily.objects.filter(
        dailySubarea=subareas, hariIni=emerg_date)
    if not defaults:
        defaults = cln_default.objects.create(defaultSubarea=subareas)
    if not harians:
        harians = cln_daily.objects.create(
            dailySubarea=subareas, hariIni=emerg_date)

for subareas in cln_subarea.objects.all():
    defaults = cln_default.objects.filter(defaultSubarea=subareas)
    harians = cln_daily.objects.filter(
        dailySubarea=subareas, hariIni=emerg_date)
    for harian in harians:
        for default in defaults:
            if harian.kondisi == '' or harian.kondisi == None:
                harian.kondisi = default.defaultKondisi
            if harian.keterangan == '' or harian.keterangan == None:
                harian.keterangan = default.defaultKeterangan
            if harian.hasilTemuan == '' or harian.keterangan == None:
                harian.hasilTemuan = default.defaultHasilTemuan
        harian.save()
