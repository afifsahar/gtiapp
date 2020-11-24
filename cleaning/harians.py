import datetime
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=cln_subarea)
def create_daily(sender, instance, created, **kwargs):
    if created:
        cln_daily.objects.create(
            dailySubarea=instance, hariIni=date.today())
        cln_default.objects.create(
            defaultSubarea=instance)
        harians = cln_daily.objects.filter(
            dailySubarea=instance, hariIni=date.today())
        defaults = cln_default.objects.filter(defaultSubarea=instance)
        for (harian, default) in zip(harians, defaults):
            harian.hariIni = datetime(
                date.today().year, date.today().month, date.today().day)  # time 00:00:00
            harian.kondisi = default.defaultKondisi
            harian.keterangan = default.defaultKeterangan
            harian.hasilTemuan = default.defaultHasilTemuan
            harian.save()


@receiver(post_save, sender=cln_subarea)
def save_daily(sender, instance, **kwargs):
    instance.dailySubarea.save()
    instance.defaultSubarea.save()


@receiver(post_save, sender=cln_subarea)
def update_daily(sender, instance, created, **kwargs):
    if created == False:
        instance.dailySubarea.save()
        instance.defaultSubarea.save()
