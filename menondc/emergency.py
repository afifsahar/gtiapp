import datetime
from datetime import date, timedelta
from menondc.models import *

emerg_date = date(2021, 1, 11)

# def cln_when_day_fail():
if not mendc_day.objects.filter(hariIni=emerg_date):
    mendc_day(hariIni=emerg_date).save()

for subareas in mendc_subarea.objects.all():
    defaults = mendc_default.objects.filter(defaultSubarea=subareas)
    harians = mendc_daily.objects.filter(
        dailySubarea=subareas, hariIni=emerg_date)
    if not defaults:
        defaults = mendc_default.objects.create(defaultSubarea=subareas)
    if not harians:
        harians = mendc_daily.objects.create(
            dailySubarea=subareas, hariIni=emerg_date)

for subareas in mendc_subarea.objects.all():
    defaults = mendc_default.objects.filter(defaultSubarea=subareas)
    harians = mendc_daily.objects.filter(
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
