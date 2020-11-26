from django.db import models
import datetime
import django
from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, gettext_lazy as __
User = get_user_model()


class mendc_day(models.Model):

    hari_ini = models.DateField(
        name="hariIni", auto_now=False, auto_now_add=False, verbose_name="Hari ini")
    mendcMaker = models.ForeignKey(User, verbose_name="Maker's Signature",
                                   on_delete=models.PROTECT, related_name="mendcMaker", blank=True, null=True, limit_choices_to={'groups__name': 'maker'})
    mendcChecker = models.ForeignKey(User, verbose_name="Checker's Signature",
                                     on_delete=models.PROTECT, related_name="mendcChecker", blank=True, null=True, limit_choices_to={'groups__name': 'checker'})
    mendcSigner = models.ForeignKey(User, verbose_name="Signer's Signature",
                                    on_delete=models.PROTECT, related_name="mendcSigner", blank=True, null=True, limit_choices_to={'groups__name': 'signer'})

    class Meta:
        verbose_name = _("day")
        verbose_name_plural = _("days")

    def __str__(self):
        return "{0}".format(self.hariIni)

    def get_absolute_url(self):
        return reverse("day_detail", kwargs={"pk": self.pk})


class mendc_area(models.Model):
    nama_area = models.CharField(max_length=100, name='namaArea',
                                 verbose_name='Nama Area', unique=True, blank=True, null=True)

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


class mendc_subarea(models.Model):
    nama_subarea = models.CharField(
        max_length=100, name='namaSubarea', verbose_name='Nama Subarea', blank=True, null=True)
    namaAreaSubarea = models.ForeignKey(
        mendc_area, verbose_name="Nama Area", on_delete=models.CASCADE, related_name="namaAreaSubarea", blank=True, null=True)

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


class mendc_default(models.Model):
    pilih_kondisi = {
        ('Ok', 'Ok'),
        ('Not Ok', 'not Ok'),
    }

    defaultSubarea = models.ForeignKey(mendc_subarea, verbose_name="Nama Subarea",
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
        return self.name

    def get_absolute_url(self):
        return reverse("default_detail", kwargs={"pk": self.pk})


class mendc_daily(models.Model):
    hari_ini = models.DateField(
        name="hariIni", auto_now=False, auto_now_add=False, verbose_name="Hari ini")
    pilih_kondisi = {
        ('Ok', 'Ok'),
        ('Not Ok', 'not Ok'),
    }
    kondisi = models.CharField(name="kondisi", max_length=50,
                               choices=pilih_kondisi, verbose_name="Kondisi", blank=True, null=True, default='')
    keterangan = models.TextField(name="keterangan", max_length=500,
                                  verbose_name="Keterangan", blank=True, null=True, default='')
    hasil_temuan = models.TextField(name="hasilTemuan", max_length=500,
                                    verbose_name="Hasil Temuan", blank=True, null=True, default='')
    done = models.DateTimeField(
        name="done", auto_now=False, auto_now_add=False, verbose_name="Terlaksana Pada", blank=True, null=True)

    dailySubarea = models.ForeignKey(mendc_subarea, verbose_name="Nama Subarea",
                                     on_delete=models.CASCADE, related_name="dailySubarea", blank=True, null=True)
    # last_update = models.DateField(
    #     name="lastUpdate", auto_now=True, auto_now_add=False, verbose_name="Last Update", blank=True, null=True)
    # sign_maker = models.BooleanField(
    #     blank=True, null=True, verbose_name="Maker's Sign", name='makerSign', default=False)
    # sign_checker = models.BooleanField(
    #     blank=True, null=True, verbose_name="Checker's Sign", name='checkerSign', default=False)
    # sign_signer = models.BooleanField(
    #     blank=True, null=True, verbose_name="Signer's Sign", name='signerSign', default=False)

    def __str__(self):
        return "{0}%{1}-{2}".format(self.hariIni, self.dailySubarea.namaSubarea, self.dailySubarea.namaAreaSubarea.namaArea)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'daily'
        verbose_name_plural = 'dailies'

    def to_dict_json(self):
        return{
            'id': self.id,
            'pk': self.pk,
            'hariIni': self.hariIni,
            'kondisiJam9': self.kondisiJam9,
            'kondisiJam14': self.kondisiJam14,
            'ketJam9': self.ketJam9,
            'ketJam14': self.ketJam14,
            'doneJam9': self.doneJam9,
            'doneJam14': self.doneJam14,
            'dailySubarea': self.dailySubarea.id,
            'namadailySubarea': self.dailySubarea.namaSubarea,
            # 'dailyArea': self.dailySubarea.namaArea.id,
            # 'namadailyArea': self.dailySubarea.namaArea,
        }


class mendc_latest_history(models.Model):
    history = models.DateField(
        name="history", auto_now=False, auto_now_add=False, verbose_name="History")

    def __str__(self):
        return "{0}".format(self.history)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'history'
        verbose_name_plural = 'histories'
