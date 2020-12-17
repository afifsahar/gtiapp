# import datetime
# from datetime import date, timedelta
# from workorder.models import *


# def workorder_when_day_create():
#     # if not mendc_day.objects.filter(hariIni=date.today()):
#     #     mendc_day(hariIni=date.today()).save()

#     for days in wo_day.objects.all():
#         defaults = mendc_default.objects.filter(defaultSubarea=subareas)
#         harians = mendc_daily.objects.filter(
#             dailySubarea=subareas, hariIni=date.today())
#         if not defaults:
#             defaults = mendc_default.objects.create(defaultSubarea=subareas)
#         if not harians:
#             harians = mendc_daily.objects.create(
#                 dailySubarea=subareas, hariIni=date.today())

#     for subareas in mendc_subarea.objects.all():
#         defaults = mendc_default.objects.filter(defaultSubarea=subareas)
#         harians = mendc_daily.objects.filter(
#             dailySubarea=subareas, hariIni=date.today())
#         for harian in harians:
#             for default in defaults:
#                 if harian.kondisi == '' or harian.kondisi == None:
#                     harian.kondisi = default.defaultKondisi
#                 if harian.keterangan == '' or harian.keterangan == None:
#                     harian.keterangan = default.defaultKeterangan
#                 if harian.hasilTemuan == '' or harian.keterangan == None:
#                     harian.hasilTemuan = default.defaultHasilTemuan
#             harian.save()