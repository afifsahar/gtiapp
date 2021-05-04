import datetime
from datetime import date, timedelta
from cleaning.models import *

mei = []
for i in range(1, 32, 1):
    mei.append(date(2021, 5, i))

# rumus range() = range(first_number,last_number,range).
# untuk bulan dengan 30 hari last_number = 31. untuk bulan dengan 31 hari, last_number = 32

for emerg_date in mei:
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
