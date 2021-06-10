from django.db import models
import datetime
import django
from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, gettext_lazy as __

User = get_user_model()


class cln_day(models.Model):

    hari_ini = models.DateField(
        name="hariIni", auto_now=False, auto_now_add=False, verbose_name="Hari ini")
    clnMaker = models.ForeignKey(User, verbose_name="Maker's Signature",
                                 on_delete=models.PROTECT, related_name="clnMaker", blank=True, null=True, limit_choices_to={'groups__name': 'maker'})
    clnChecker = models.ForeignKey(User, verbose_name="Checker's Signature",
                                   on_delete=models.PROTECT, related_name="clnChecker", blank=True, null=True, limit_choices_to={'groups__name': 'checker'})
    clnSigner = models.ForeignKey(User, verbose_name="Signer's Signature",
                                  on_delete=models.PROTECT, related_name="clnSigner", blank=True, null=True, limit_choices_to={'groups__name': 'signer'})

    class Meta:
        verbose_name = _("day")
        verbose_name_plural = _("days")

    def __str__(self):
        return "{0}".format(self.hariIni)

    # def get_absolute_url(self):
    #     return reverse("day_detail", kwargs={"pk": self.pk})


class cln_area(models.Model):
    nama_area = models.CharField(max_length=100, name='namaArea',
                                 verbose_name='Nama Area', unique=True, blank=False, null=False)
    # areaDay = models.ForeignKey(cln_day, verbose_name="areaDay",
    #                             on_delete=models.CASCADE, related_name="areaDay", blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.namaArea)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'area'
        verbose_name_plural = 'areas'

    def to_dict_json(self):
        return{
            'id': self.id,
            'pk': self.pk,
            'namaArea': self.namaArea,
        }


class cln_subarea(models.Model):
    nama_subarea = models.CharField(
        max_length=100, name='namaSubarea', verbose_name='Nama Subarea', blank=False, null=False, unique=False)
    namaAreaSubarea = models.ForeignKey(
        cln_area, verbose_name="Nama Area", on_delete=models.CASCADE, related_name="namaAreaSubarea", blank=True, null=True)

    def __str__(self):
        return "{0} % {1}".format(self.namaSubarea, self.namaAreaSubarea.namaArea)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'subarea'
        verbose_name_plural = 'subareas'

    def to_dict_json(self):
        return{
            'id': self.id,
            'pk': self.pk,
            'namaSubarea': self.namaSubarea,
            'namaAreaSubarea': self.namaAreaSubarea.namaArea,
        }

# class cln_dailyManager(models.Manager):


class cln_default(models.Model):
    pilih_kondisi = (
        ('Ok', 'Ok'),
        ('Not Ok', 'Not Ok'),
    )
    defaultSubarea = models.ForeignKey(cln_subarea, verbose_name="Nama Subarea",
                                       on_delete=models.CASCADE, related_name="defaultSubarea", blank=True, null=True)
    defaultKondisi = models.CharField(name="defaultKondisi", max_length=50,
                                      choices=pilih_kondisi, verbose_name="Kondisi", blank=True, null=True, default='')
    defaultKeterangan = models.TextField(name="defaultKeterangan", max_length=500,
                                         verbose_name="Keterangan", blank=True, null=True, default='')
    defaultHasilTemuan = models.TextField(name="defaultHasilTemuan", max_length=500,
                                          verbose_name="Hasil Temuan", blank=True, null=True, default='')
    # last_update = models.DateField(
    #     name="lastUpdate", auto_now=True, auto_now_add=False, verbose_name="Last Update", blank=True, null=True)

    class Meta:
        verbose_name = _("default")
        verbose_name_plural = _("defaults")

    def __str__(self):
        return "{0}-{1}".format(self.defaultSubarea.namaSubarea, self.defaultSubarea.namaAreaSubarea.namaArea)

    # def get_absolute_url(self):
    #     return reverse("default_detail", kwargs={"pk": self.pk})


class cln_daily(models.Model):
    hari_ini = models.DateField(
        name="hariIni", auto_now=False, auto_now_add=False, verbose_name="Hari ini")
    pilih_kondisi = (
        ('Ok', 'Ok'),
        ('Not Ok', 'Not Ok'),
    )
    kondisi = models.CharField(name="kondisi", max_length=50,
                               choices=pilih_kondisi, verbose_name="Kondisi", blank=True, null=True, default='')
    keterangan = models.TextField(name="keterangan", max_length=500,
                                  verbose_name="Keterangan", blank=True, null=True, default='')
    hasil_temuan = models.TextField(name="hasilTemuan", max_length=500,
                                    verbose_name="Hasil Temuan", blank=True, null=True, default='')
    done = models.DateTimeField(
        name="done", auto_now=False, auto_now_add=False, verbose_name="Terlaksana Pada", blank=True, null=True)
    dailySubarea = models.ForeignKey(cln_subarea, verbose_name="Nama Subarea",
                                     on_delete=models.CASCADE, related_name="dailySubarea", blank=True, null=True)
    # last_update = models.DateField(
    #     name="lastUpdate", auto_now=True, auto_now_add=False, verbose_name="Last Update", blank=True, null=True)

    def __str__(self):
        return "{0}%{1}-{2}".format(self.hariIni, self.dailySubarea.namaSubarea, self.dailySubarea.namaAreaSubarea.namaArea)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'daily'
        verbose_name_plural = 'dailies'


class cln_latest_history(models.Model):
    history = models.DateField(
        name="history", auto_now=False, auto_now_add=False, verbose_name="History")

    def __str__(self):
        return "{0}".format(self.history)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'history'
        verbose_name_plural = 'histories'
