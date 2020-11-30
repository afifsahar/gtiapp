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
        for harian in harians:
            for default in defaults:
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
        for harian in harians:
            for default in defaults:
                if harian.kondisi == '' or harian.kondisi == None:
                    harian.kondisi = default.defaultKondisi
                if harian.keterangan == '' or harian.keterangan == None:
                    harian.keterangan = default.defaultKeterangan
                if harian.hasilTemuan == '' or harian.keterangan == None:
                    harian.hasilTemuan = default.defaultHasilTemuan