import datetime
from datetime import date, timedelta
from cleaning.models import *
import pytz
from django.utils import timezone as tz
from pytz import timezone
from django.utils import timezone as tz
from django.conf import settings


def create_area():
    mei = []
    for i in range(1, 32, 1):
        mei.append(date(2021, 5, i))

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


def cln_alterfield():
    jakarta = timezone('Asia/Jakarta')
    # make_aware(naive, timezone=pytz.timezone("Europe/Helsinki"))

    for day in cln_day.objects.all():
        day.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(day.hariIni, datetime.min.time()))
        day.deleteAt = datetime(year=2050, month=12,
                                day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        day.save()
    for area in cln_area.objects.all():
        area.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0))
        # datetime(year=2021, month=1,
        #                          day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        area.deleteAt = datetime(year=2050, month=12,
                                 day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        area.save()
    for subarea in cln_subarea.objects.all():
        subarea.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        subarea.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        subarea.save()
    for harian in cln_daily.objects.all():
        harian.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(harian.hariIni, datetime.min.time()))
        harian.deleteAt = datetime(year=2050, month=12,
                                   day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        harian.save()
    for default in cln_default.objects.all():
        default.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        default.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        default.save()
    for history in cln_latest_history.objects.all():
        history.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        history.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        history.save()


def cln_area_delete_revive(self, area_id):
    areas = cln_area.objects.get(id=self.area_id, isDelete=True)
    subareas = cln_subarea.objects.filter(namaAreaSubarea=areas, isDelete=True)
    for subarea in subareas:
        for default in cln_default.objects.filter(defaultSubarea=subarea, isDelete=True):
            default.isDelete = False
            default.deleteAt = datetime(
                year=2050, month=12, day=31, hour=23, minute=59, second=59)
        for daily in cln_daily.objects.filter(dailySubarea=subarea, isDelete=True):
            daily.isDelete = False
            daily.deleteAt = datetime(
                year=2050, month=12, day=31, hour=23, minute=59, second=59)
        subarea.isDelete = False
        subarea.deleteAt = datetime(
            year=2050, month=12, day=31, hour=23, minute=59, second=59)
    areas.isDelete = False
    areas.deleteAt = date.today()
    areas.save()


def cln_when_day_change():
    if not cln_day.objects.filter(isDelete=False, hariIni=date.today()):
        cln_day(hariIni=date.today()).save()

    for subareas in cln_subarea.objects.filter(isDelete=False):
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

    for subareas in cln_subarea.objects.filter(isDelete=False):
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
            harian.save()

# when area and subarea are created
# 1. create today daily
# 2. create default fk to area and subarea


def cln_when_create_subarea():
    for subareas in cln_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

# when set default
# 1. fill today daily keterangan with created default value only if today daily is blank


def cln_when_set_default():
    for subareas in cln_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
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
            harian.save()


def cln_when_date_change(date):
    if not cln_day.objects.filter(hariIni=date):
        cln_day(hariIni=date).save()

    for subareas in cln_subarea.objects.filter(isDelete=False):
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date)
        if not defaults:
            defaults = cln_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = cln_daily.objects.create(
                dailySubarea=subareas, hariIni=date)

    for subareas in cln_subarea.objects.filter(isDelete=False):
        defaults = cln_default.objects.filter(defaultSubarea=subareas)
        harians = cln_daily.objects.filter(
            dailySubarea=subareas, hariIni=date)
        for harian in harians:
            for default in defaults:
                if harian.kondisi == '' or harian.kondisi == None:
                    harian.kondisi = default.defaultKondisi
                if harian.keterangan == '' or harian.keterangan == None:
                    harian.keterangan = default.defaultKeterangan
                if harian.hasilTemuan == '' or harian.keterangan == None:
                    harian.hasilTemuan = default.defaultHasilTemuan
            harian.save()


def five_oclock():
    mid = datetime.min.time()  # midnight
    delta = timedelta(hours=5)  # plus 5 hours
    five = (datetime.combine(date(1, 1, 1), mid)+delta).time()
    return five
