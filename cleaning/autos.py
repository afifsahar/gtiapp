import datetime
from datetime import date, timedelta
from cleaning.models import *

def cln_when_day_change():
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
        for (harian,default) in zip(harians,defaults):
            if harian.hariIni == '' or harian.hariIni == None:
                harian.hariIni = datetime(date.today().year, date.today().month, date.today().day)  # time 00:00:00
            if harian.kondisi == '' or harian.kondisi == None:
                harian.kondisi = default.defaultKondisi
            if harian.keterangan == '' or harian.keterangan == None:
                harian.keterangan = default.defaultKeterangan
            if harian.hasilTemuan == '' or harian.keterangan == None:
                harian.hasilTemuan = default.defaultHasilTemuan

## when area and subarea are created
# 1. create today daily
# 2. create default fk to area and subarea
def cln_when_create_subarea():
    for subareas in cln_subarea.objects.all():
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

## when set default
# 1. fill today daily keterangan with created default value only if today daily is blank
def cln_when_set_default():
    for subareas in cln_subarea.objects.all():
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        for (harian, default) in zip(harians, defaults):
            if harian.hariIni == '' or harian.hariIni == None:
                harian.hariIni = datetime(date.today().year, date.today().month, date.today().day)  # time 00:00:00
            if harian.kondisi == '' or harian.kondisi == None:
                harian.kondisi = default.defaultKondisi
            if harian.keterangan == '' or harian.keterangan == None:
                harian.keterangan = default.defaultKeterangan
            if harian.hasilTemuan == '' or harian.keterangan == None:
                harian.hasilTemuan = default.defaultHasilTemuan

# def area_subarea_dict():
#     areadict = dict()
#     for areas in cln_area.objects.all():
#         for (subareas,i) in zip(cln_subarea.objects.filter(namaAreaSubarea=areas), range(1, (cln_subarea.objects.filter(namaAreaSubarea=areas).count()+1))):
#             areadict.update({areas:{subareas:i}})
#     return areadict