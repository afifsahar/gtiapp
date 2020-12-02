import datetime
from datetime import date, timedelta
from menondc.models import *

## when day change
# 1. create today
# 2. create daily fk to area and subarea
# 3. fill daily with existing default value
def mendc_when_day_change():
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
        for harian in harians:
            for default in defaults:
                if harian.kondisi == '' or harian.kondisi == None:
                    harian.kondisi = default.defaultKondisi
                if harian.keterangan == '' or harian.keterangan == None:
                    harian.keterangan = default.defaultKeterangan
                if harian.hasilTemuan == '' or harian.keterangan == None:
                    harian.hasilTemuan = default.defaultHasilTemuan
            harian.save()
## when area and subarea are created
# 1. create today daily
# 2. create default fk to area and subarea
def cln_when_create_subarea():
    for subareas in mendc_subarea.objects.all():
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = mendc_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = mendc_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

## when set default
# 1. fill today daily keterangan with created default value only if today daily is blank
def cln_when_set_default():
    for subareas in mendc_subarea.objects.all():
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        for harian in harians:
            for default in defaults:
                if harian.kondisi == '' or harian.kondisi == None:
                    harian.kondisi = default.defaultKondisi
                if harian.keterangan == '' or harian.keterangan == None:
                    harian.keterangan = default.defaultKeterangan
                if harian.hasilTemuan == '' or harian.keterangan == None:
                    harian.hasilTemuan = default.defaultHasilTemuan
            harian.save()

# def area_subarea_dict():
#     areadict = dict()
#     for areas in mendc_area.objects.all():
#         for (subareas,i) in zip(mendc_subarea.objects.filter(namaAreaSubarea=areas), range(1, (mendc_subarea.objects.filter(namaAreaSubarea=areas).count()+1))):
#             areadict.update({areas:{subareas:i}})
#     return areadict
