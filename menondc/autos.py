import datetime
from datetime import date, timedelta
from .models import *

if not mendc_day.objects.filter(hariIni=date.today()):
    mendc_day(hariIni=date.today()).save()

for subareas in mendc_subarea.objects.all():
    defaults = mendc_default.objects.filter(defaultSubarea=subareas)
    harians = mendc_daily.objects.filter(
        dailySubarea=subareas, hariIni=date.today())
    if not defaults:
        defaults = mendc_default.objects.create(defaultSubarea=subareas)
    if not harians:
        harians = mendc_daily.objects.create(
            dailySubarea=subareas, hariIni=date.today())

for subareas in mendc_subarea.objects.all():
    defaults = mendc_default.objects.filter(defaultSubarea=subareas)
    harians = mendc_daily.objects.filter(
        dailySubarea=subareas, hariIni=date.today())
    for default in defaults:
        harians.hariIni = datetime(
            date.today().year, date.today().month, date.today().day)  # time 00:00:00
        harians.kondisi = default.defaultKondisi
        harians.keterangan = default.defaultKeterangan
        harians.hasilTemuan = default.defaultHasilTemuan