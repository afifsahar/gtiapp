import datetime
from datetime import date, timedelta
from menondc.models import *
import pytz
from django.utils import timezone as tz
from pytz import timezone


def mendc_maker_sign():
    # rez = [
    #     date(2021, 2, 3), date(2021, 2, 4), date(2021, 2, 10), date(
    #         2021, 2, 11), date(2021, 2, 23), date(2021, 2, 24)
    #     # date(2021, 3, 1), date(2021, 3, 2), date(2021, 3, 5), date(2021, 3, 8), date(2021, 3, 12), date(2021, 3, 15), date(
    #     #     2021, 3, 18), date(2021, 3, 19), date(2021, 3, 22), date(2021, 3, 23), date(2021, 3, 26), date(2021, 3, 29),
    #     # date(2021, 4, 1), date(2021, 3, 7), date(2021, 3, 8), date(2021, 3, 13), date(2021, 3, 14), date(
    #     #     2021, 3, 19), date(2021, 3, 20), date(2021, 3, 23), date(2021, 3, 26), date(2021, 3, 29), date(2021, 3, 30)
    # ]
    rez = [date(2021, 1, 5), date(2021, 1, 7), date(2021, 1, 11), date(2021, 1, 13), date(2021, 1, 14), date(2021, 1, 15), date(2021, 1, 18), date(2021, 1, 20), date(2021, 1, 21), date(2021, 1, 26), date(2021, 1, 27),
           date(2021, 2, 3), date(2021, 2, 4), date(2021, 2, 10), date(
               2021, 2, 11), date(2021, 2, 23), date(2021, 2, 24),
           date(2021, 3, 1), date(2021, 3, 2), date(2021, 3, 5), date(2021, 3, 8), date(2021, 3, 12), date(2021, 3, 15), date(
               2021, 3, 18), date(2021, 3, 19), date(2021, 3, 22), date(2021, 3, 23), date(2021, 3, 26), date(2021, 3, 29),
           date(2021, 4, 1), date(2021, 3, 7), date(2021, 3, 8), date(2021, 3, 13), date(2021, 3, 14), date(
        2021, 3, 19), date(2021, 3, 20), date(2021, 3, 23), date(2021, 3, 26), date(2021, 3, 29), date(2021, 3, 30),
        date(2021, 5, 5), date(2021, 5, 6), date(2021, 5, 10), date(2021, 5, 18), date(
        2021, 5, 19), date(2021, 5, 21), date(2021, 5, 25), date(2021, 5, 27), date(2021, 5, 31),
        date(2021, 6, 4), date(2021, 6, 4), date(2021, 6, 4), date(2021, 6, 4), date(
        2021, 6, 4), date(2021, 6, 4), date(2021, 6, 4), date(2021, 6, 4), date(2021, 6, 4),
        date(2021, 7, 1), date(2021, 7, 6), date(2021, 7, 9), date(2021, 7, 12), date(
        2021, 7, 14), date(2021, 7, 19), date(2021, 7, 21), date(2021, 7, 26),
    ]
    for rez_date in rez:
        for day in mendc_day.objects.filter(hariIni=rez_date):
            day.mendcMaker = User.objects.get(username="Rezki")
            day.mendcSigner = User.objects.get(username="Hendrymaster")
            day.mendcChecker = User.objects.get(username="dhona")
            day.save()

    for day in mendc_day.objects.all():
        if day.mendcMaker == "" or day.mendcSigner == None:
            day.mendcMaker = User.objects.get(username="trisatria")
            day.mendcSigner = User.objects.get(username="Hendrymaster")
            day.mendcChecker = User.objects.get(username="dhona")
            day.save()


def create_area():
    feb = []
    for i in range(1, 29, 1):
        feb.append(date(2021, 2, i))

    for emerg_date in feb:
        if not mendc_day.objects.filter(hariIni=emerg_date):
            mendc_day(hariIni=emerg_date).save()

            for subareas in mendc_subarea.objects.all():
                defaults = mendc_default.objects.filter(
                    defaultSubarea=subareas)
                harians = mendc_daily.objects.filter(
                    dailySubarea=subareas, hariIni=emerg_date)
                if not defaults:
                    defaults = mendc_default.objects.create(
                        defaultSubarea=subareas)
                if not harians:
                    harians = mendc_daily.objects.create(
                        dailySubarea=subareas, hariIni=emerg_date)
        for subareas in mendc_subarea.objects.all():
            defaults = mendc_default.objects.filter(defaultSubarea=subareas)
            harians = mendc_daily.objects.filter(
                dailySubarea=subareas, hariIni=emerg_date)
            for harian in harians:
                for default in defaults:
                    harian.kondisi = "Ok"
                    # if harian.kondisi == '' or harian.kondisi == None:
                    # harian.kondisi = default.defaultKondisi
                    # harian.kondisi = "Ok"
                    if harian.keterangan == '' or harian.keterangan == None:
                        harian.keterangan = default.defaultKeterangan
                    if harian.hasilTemuan == '' or harian.keterangan == None:
                        harian.hasilTemuan = default.defaultKeterangan
                    else:
                        harian.kondisi = "Not Ok"
                harian.save()
        # mendc_maker_sign()


def mendc_alterfield():
    jakarta = timezone('Asia/Jakarta')
    # make_aware(naive, timezone=pytz.timezone("Europe/Helsinki"))
    for day in mendc_day.objects.all():
        day.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(day.hariIni, datetime.min.time()))
        day.deleteAt = datetime(year=2050, month=12,
                                day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        day.save()
    for area in mendc_area.objects.all():
        area.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime(year=2021, month=1, day=1, hour=0, minute=0, second=0))
        area.deleteAt = datetime(year=2050, month=12,
                                 day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        area.save()
    for subarea in mendc_subarea.objects.all():
        subarea.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        subarea.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        subarea.save()
    for harian in mendc_daily.objects.all():
        harian.createAt = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(harian.hariIni, datetime.min.time()))
        harian.deleteAt = datetime(year=2050, month=12,
                                   day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        harian.save()
    for default in mendc_default.objects.all():
        default.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        default.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        default.save()
    for history in mendc_latest_history.objects.all():
        history.createAt = datetime(year=2021, month=1,
                                    day=1, hour=0, minute=0, second=0, tzinfo=timezone(settings.TIME_ZONE))
        history.deleteAt = datetime(year=2050, month=12,
                                    day=31, hour=23, minute=59, second=59, tzinfo=timezone(settings.TIME_ZONE))
        history.save()


def mendc_area_delete_revive(self, area_id):
    areas = mendc_area.objects.get(id=self.area_id, isDelete=True)
    subareas = mendc_subarea.objects.filter(
        namaAreaSubarea=areas, isDelete=True)
    for subarea in subareas:
        for default in mendc_default.objects.filter(defaultSubarea=subarea, isDelete=True):
            default.isDelete = False
            default.deleteAt = datetime(
                year=2050, month=12, day=31, hour=23, minute=59, second=59)
        for daily in mendc_daily.objects.filter(dailySubarea=subarea, isDelete=True):
            daily.isDelete = False
            daily.deleteAt = datetime(
                year=2050, month=12, day=31, hour=23, minute=59, second=59)
        subarea.isDelete = False
        subarea.deleteAt = datetime(
            year=2050, month=12, day=31, hour=23, minute=59, second=59)
    areas.isDelete = False
    areas.deleteAt = date.today()
    areas.save()


def mendc_when_day_change():
    if not mendc_day.objects.filter(createAt__date__lte=date.today(), isDelete=False, hariIni=date.today()):
        mendc_day(hariIni=date.today()).save()

    for subareas in mendc_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = mendc_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = mendc_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

    for subareas in mendc_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
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

# when area and subarea are created
# 1. create today daily
# 2. create default fk to area and subarea


def mendc_when_create_subarea():
    for subareas in mendc_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date.today())
        if not defaults:
            defaults = mendc_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = mendc_daily.objects.create(
                dailySubarea=subareas, hariIni=date.today())

# when set default
# 1. fill today daily keterangan with created default value only if today daily is blank


def mendc_when_set_default():
    for subareas in mendc_subarea.objects.filter(createAt__date__lte=date.today(), isDelete=False):
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


def mendc_when_date_change(date):
    if not mendc_day.objects.filter(hariIni=date):
        mendc_day(hariIni=date).save()

    for subareas in mendc_subarea.objects.filter(isDelete=False):
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
            dailySubarea=subareas, hariIni=date)
        if not defaults:
            defaults = mendc_default.objects.create(defaultSubarea=subareas)
        if not harians:
            harians = mendc_daily.objects.create(
                dailySubarea=subareas, hariIni=date)

    for subareas in mendc_subarea.objects.filter(isDelete=False):
        defaults = mendc_default.objects.filter(defaultSubarea=subareas)
        harians = mendc_daily.objects.filter(
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
