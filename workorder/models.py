from django.db import models
import django
import datetime
from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, gettext_lazy as __
from multiselectfield import MultiSelectField

User = get_user_model()


class wo_day(models.Model):

    last_update = models.DateTimeField(
        _("Last Update"), name="lastUpdate", auto_now=True, auto_now_add=False)
    create_at = models.DateTimeField(
        _("Create At"), name="createAt", auto_now=False, auto_now_add=True)
    is_delete = models.BooleanField(
        _("Is Delete"), name="isDelete", null=True, blank=True, default=False)

    class Meta:
        verbose_name = _("day")
        verbose_name_plural = _("days")

    def __str__(self):
        return "WO {0}".format(self.createAt)

    def get_absolute_url(self):
        return reverse("day_detail", kwargs={"pk": self.pk})


class wo_description(models.Model):
    area_choice = (
        ('Lt.UG', 'Lt.UG'),
        ('Lt.1', 'Lt.1'),
        ('Lt.2', 'Lt.2'),
        ('Lt.3', 'Lt.3'),
        ('Lt.4', 'Lt.4'),
        ('Lt.5', 'Lt.5'),
        ('Lt.6', 'Lt.6'),
        ('Lt.7', 'Lt.7'),
        ('Lt.8', 'Lt.8'),
        ('Lt.9', 'Lt.9'),
    )
    category_service = (
        ('Mechanical', 'Mechanical'),
        ('Electrical', 'Electrical'),
        ('Security', 'Security'),
        ('Cleaning', 'Cleaning'),
        ('Sivil/Architectur', 'Sivil/Architectur'),
        ('Electronics', 'Electronics'),
        ('Others', 'Others'),
    )
    last_update = models.DateTimeField(
        _("Last Update"), name="lastUpdate", auto_now=True, auto_now_add=False)
    create_at = models.DateTimeField(
        _("Create At"), name="createAt", auto_now=False, auto_now_add=True)
    is_delete = models.BooleanField(
        _("Is Delete"), name="isDelete", null=True, blank=True, default=False)
    woUser = models.ForeignKey(User, verbose_name=_("WO User"), name="woUser", on_delete=models.PROTECT,
                               null=True, blank=True, limit_choices_to={'groups__name': 'maker'})
    division = models.CharField(
        _("Division"), max_length=10, null=True, blank=True, default="OSP")
    # area = models.CharField(
    #     _("Area"), name='area', choices=area_choice, max_length=20, null=True, blank=True)
    # categoryService = models.CharField(_("Category Service"), name='categoryService',
    #                                    choices=category_service, max_length=20, null=True, blank=True)
    area = MultiSelectField(
        _("Area"), name='area', choices=area_choice, null=True, blank=True)
    categoryService = MultiSelectField(_("Category Service"), name='categoryService',
                                       choices=category_service, null=True, blank=True)
    csOthers=models.CharField(_("Category Service Others"), name='csOthers',max_length=20, null=True, blank=True, default='')
    description = models.TextField(
        _("Description"), null=True, blank=True, max_length=1000, name="description")
    descriptionDay = models.ForeignKey(wo_day, verbose_name=_(
        "Description Day"), related_name="descriptionDay", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("description")
        verbose_name_plural = _("descriptions")

    def __str__(self):
        return "Description {0}".format(self.createAt)

    def get_absolute_url(self):
        return reverse("description_detail", kwargs={"pk": self.pk})


class wo_workorder(models.Model):
    last_update = models.DateTimeField(
        _("Last Update"), name="lastUpdate", auto_now=True, auto_now_add=False)
    create_at = models.DateTimeField(
        _("Create At"), name="createAt", auto_now=False, auto_now_add=True)
    is_delete = models.BooleanField(
        _("Is Delete"), name="isDelete", null=True, blank=True, default=False)
    woMaker = models.ForeignKey(User, verbose_name=_("WO Maker"), related_name="woMaker",
                                on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'maker'})
    woChecker = models.ForeignKey(User, verbose_name=_("WO Checker"), related_name="woChecker",
                                  on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'checker'})
    woSigner = models.ForeignKey(User, verbose_name=_("WO Signer"), related_name="woSigner",
                                 on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'signer'})
    workorder = models.TextField(
        _("Work Order"), name="workorder", max_length=1000, null=True, blank=True)
    duration = models.CharField(
        _("Duration"), max_length=50, null=True, blank=True, name="duration")
    due_date = models.DateField(
        _("Due Date"), auto_now=False, auto_now_add=False, name="dueDate")
    workorderDay = models.ForeignKey(wo_day, verbose_name=_(
        "Work Order Day"), related_name="workorderDay", on_delete=models.PROTECT, null=True, blank=True)
    workorderDescription = models.ForeignKey(wo_description, verbose_name=_(
        "Work Order Description"), related_name="workorderDescription", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("work order")
        verbose_name_plural = _("work orders")

    def __str__(self):
        return "Work Order {0}".format(self.createAt)

    def get_absolute_url(self):
        return reverse("workorder_detail", kwargs={"pk": self.pk})


class wo_progress(models.Model):
    last_update = models.DateTimeField(
        _("Last Update"), name="lastUpdate", auto_now=True, auto_now_add=False)
    create_at = models.DateTimeField(
        _("Create At"), name="createAt", auto_now=False, auto_now_add=True)
    is_delete = models.BooleanField(
        _("Is Delete"), name="isDelete", null=True, blank=True, default=False)
    woBriks = models.ForeignKey(User, verbose_name=_("WO BRIKS"), related_name="woBriks",
                                on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'briks'})
    progressDay = models.ForeignKey(wo_day, verbose_name=_(
        "Progress Day"), related_name="progressDay", on_delete=models.PROTECT, null=True, blank=True)
    progressDescription = models.ForeignKey(wo_description, verbose_name=_(
        "Progress Description"), related_name="progressDescription", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("progress")
        verbose_name_plural = _("progresss")

    def __str__(self):
        return "Progress {0}".format(self.createAt)

    def get_absolute_url(self):
        return reverse("progress_detail", kwargs={"pk": self.pk})


class wo_rincian(models.Model):
    last_update = models.DateTimeField(
        _("Last Update"), name="lastUpdate", auto_now=True, auto_now_add=False)
    create_at = models.DateTimeField(
        _("Create At"), name="createAt", auto_now=False, auto_now_add=True)
    is_delete = models.BooleanField(
        _("Is Delete"), name="isDelete", null=True, blank=True, default=False)
    date = models.DateField(_("Date"), name="date", auto_now=False,
                            auto_now_add=False, null=True, blank=True)
    status = models.CharField(
        _("Status"), name="status", max_length=50, null=True, blank=True)
    information = models.TextField(
        _("Information"), name="information", max_length=500, null=True, blank=True)
    briksUser = models.ForeignKey(User, verbose_name=_("Petugas BRIKS"), related_name="briksUser",
                                  on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'briks'}, default='')
    ospUser = models.ForeignKey(User, verbose_name=_("Petugas OSP"), related_name="ospUser",
                                on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'groups__name': 'maker'}, default='')
    rincianProgress = models.ForeignKey(wo_progress, verbose_name=_(
        "Rincian Progress"), related_name="rincianProgress", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = _("rincian")
        verbose_name_plural = _("rincians")

    def __str__(self):
        return "Rincian {0}".format(self.createAt)

    def get_absolute_url(self):
        return reverse("rincian_detail", kwargs={"pk": self.pk})
