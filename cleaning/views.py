from django.shortcuts import render, redirect
from user.models import user_bri_image
from user.decorators import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.models import *
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .utils import render_to_pdf
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime, date
import datetime
from .forms import *
from django.forms import modelformset_factory
from .models import *
from .function import *
from django.db.models import Q


@login_required(login_url='user_login')
def cln_home(request):
    context = {
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_home.html', context)


@login_required(login_url='user_login')
def cln_settings(request):
    areas = cln_area.objects.filter(isDelete=False)
    subareas = cln_subarea.objects.filter(isDelete=False)
    areaCount = areas.count()
    context = {
        "areas": areas,
        "subareas": subareas,
        "areaCount": areaCount,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_settings.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_area_add(request):
    SubareaFormSet = modelformset_factory(cln_subarea, form=subareaForm, exclude=(
        'namaAreaSubarea',), can_delete=False, extra=1)
    if request.method == "POST":
        formset = SubareaFormSet(request.POST or None,
                                 queryset=cln_subarea.objects.none(), prefix='subarea')
        form = areaForm(request.POST or None)
        if formset.is_valid() and form.is_valid():
            areas = form.save(commit=False)
            areas.save()
            for f in formset:
                subareas = f.save(commit=False)
                subareas.namaAreaSubarea = areas
                subareas.save()
            cln_when_create_subarea()
            messages.success(
                request, 'New Area in Checklist Kebersihan Successfully Added')
            return redirect('cln_settings')
    else:
        messages.warning(
            request, 'New Area FAILED to be Added')
        formset = SubareaFormSet(
            queryset=cln_subarea.objects.none(), prefix='subarea')
        form = areaForm()
    context = {
        'form': form,
        'formset': formset,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_area_add.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_area_edit(request, area_id):
    areas = cln_area.objects.get(id=area_id, isDelete=False)
    SubareaFormSet = modelformset_factory(cln_subarea, form=subareaForm, exclude=(
        'namaAreaSubarea',), can_delete=False, extra=0)
    if request.method == "POST":
        formset = SubareaFormSet(request.POST,
                                 queryset=cln_subarea.objects.filter(namaAreaSubarea=areas.id), prefix='subarea')
        form = areaForm(request.POST, instance=areas)
        if formset.is_valid() and form.is_valid():
            ar = form.save(commit=False)
            ar.save()
            for f in formset:
                subar = f.save(commit=False)
                subar.namaAreaSubarea = ar
                subar.save()
            return redirect('cln_settings')
    else:
        formset = SubareaFormSet(queryset=cln_subarea.objects.filter(
            namaAreaSubarea=areas.id), prefix='subarea')
        form = areaForm(instance=areas)
    context = {
        'form': form,
        'formset': formset,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_area_edit.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_area_delete(request, area_id):
    areas = cln_area.objects.get(id=area_id, isDelete=False)
    subareas = cln_subarea.objects.filter(
        namaAreaSubarea=areas, isDelete=False)
    context = {
        'areas': areas,
        'subareas': subareas,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_area_delete.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_area_delete_confirm(request, area_id):
    areas = cln_area.objects.get(id=area_id, isDelete=False)
    subareas = cln_subarea.objects.filter(
        namaAreaSubarea=areas, isDelete=False)
    areas.isDelete = True
    areas.deleteAt = date.today()
    areas.save()
    for subarea in subareas:
        for default in cln_default.objects.filter(defaultSubarea=subarea, isDelete=False):
            default.isDelete = True
            default.deleteAt = datetime.now()
        for daily in cln_daily.objects.filter(dailySubarea=subarea, isDelete=False):
            daily.isDelete = True
            daily.deleteAt = datetime.now()
        subarea.isDelete = True
        subarea.deleteAt = datetime.now()
    return redirect('cln_settings')


@login_required(login_url='user_login')
def cln_progress(request):
    today_date = pytz.timezone(settings.TIME_ZONE).localize(
        datetime.combine(date.today(), datetime.min.time()))
    areas = cln_area.objects.filter(
        createAt__lte=today_date, isDelete=False)
    subareas = cln_subarea.objects.filter(
        createAt__lte=today_date, isDelete=False)
    harians = cln_daily.objects.filter(hariIni=date.today(), isDelete=False)
    days = None
    if request.user.groups.all().first().name == 'maker':
        days = cln_day.objects.filter(Q(hariIni=date.today()) & Q(clnMaker__isnull=True) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    if request.user.groups.all().first().name == 'checker':
        days = cln_day.objects.filter(Q(hariIni=date.today()) & Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    if request.user.groups.all().first().name == 'signer':
        days = cln_day.objects.filter(Q(hariIni=date.today()) & Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=False) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': harians,
        'tanggal': date.today(),
        'areaCount': areas.count(),
        'title': 'Checklist Kebersihan',
        'days': days,
        'harianCount': harians.count(),
    }
    return render(request, 'cleaning/cln_progress.html', context)


@login_required(login_url='user_login')
def cln_harian_zero(request):
    cln_when_day_change()  # Nanti Dicek lagi ya
    harians = cln_daily.objects.filter(hariIni=date.today(), isDelete=False)
    return redirect('cln_progress')


@login_required(login_url='user_login')
def cln_history_zero(request):
    obj = cln_latest_history.objects.get(id=1, isDelete=False)
    cln_when_date_change(obj.history)  # Nanti Dicek lagi ya
    return redirect('cln_history')


@login_required(login_url='user_login')
def cln_history(request):
    obj = cln_latest_history.objects.get(id=1, isDelete=False)
    if request.method == 'POST':
        tgl = request.POST.get('history')
        if tgl:
            tanggal = datetime.strptime(tgl, '%d-%m-%Y')
            tanggal.strftime('%Y-%m-%d')
            obj.history = tanggal
            obj.save()
    history_date = pytz.timezone(settings.TIME_ZONE).localize(
        datetime.combine(obj.history, datetime.min.time()))
    areas = cln_area.objects.filter(
        Q(createAt__lte=history_date) & Q(deleteAt__gt=history_date))
    subareas = cln_subarea.objects.filter(
        Q(createAt__lte=history_date) & Q(deleteAt__gt=history_date))
    dailies = cln_daily.objects.filter(Q(hariIni=obj.history))
    days = None
    if request.user.groups.all().first().name == 'maker':
        days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=True) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    if request.user.groups.all().first().name == 'checker':
        days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    if request.user.groups.all().first().name == 'signer':
        days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=False) & Q(clnSigner__isnull=True) & Q(isDelete=False))
    print(obj.history)

    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': dailies,
        'tanggalstr': obj.history.strftime('%Y-%m-%d'),
        'tanggal': obj.history,
        'harianCount': dailies.count(),
        'title': 'Checklist Kebersihan',
        'days': days,
    }
    return render(request, 'cleaning/cln_history.html', context)

# @login_required(login_url='user_login')
# def cln_history(request):
#     areas = cln_area.objects.all()
#     subareas = cln_subarea.objects.all()
#     obj = cln_latest_history.objects.get(id=1)
#     if request.method == 'POST':
#         tgl = request.POST.get('history')
#         if tgl:
#             tanggal = datetime.strptime(tgl, '%d-%m-%Y')
#             tanggal.strftime('%Y-%m-%d')
#             obj.history = tanggal
#             obj.save()
#     dailies = cln_daily.objects.filter(hariIni=obj.history)
#     days = None
#     if request.user.groups.all().first().name == 'maker':
#         days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=True) & Q(
#             clnChecker__isnull=True) & Q(clnSigner__isnull=True))
#     if request.user.groups.all().first().name == 'checker':
#         days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=False) & Q(
#             clnChecker__isnull=True) & Q(clnSigner__isnull=True))
#     if request.user.groups.all().first().name == 'signer':
#         days = cln_day.objects.filter(Q(hariIni=obj.history) & Q(clnMaker__isnull=False) & Q(
#             clnChecker__isnull=False) & Q(clnSigner__isnull=True))
#     context = {
#         # 'h_form': h_form,
#         'areas': areas,
#         'subareas': subareas,
#         'harians': dailies,
#         'tanggal': obj.history,
#         'areaCount': dailies.count(),
#         'title': 'Checklist Gedung',
#         'days': days,
#         'harianCount': dailies.count(),
#     }
#     return render(request, 'cleaning/cln_history.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_progress_check_single(request, harian_id):
    harian = cln_daily.objects.get(id=harian_id)
    if request.method == 'POST':
        form = dailyForm(request.POST or None, instance=harian)
        if form.is_valid():
            form.save(commit=False)
            if harian.kondisi != '' or harian.keterangan != '' or harian.hasilTemuan != '':
                tmsm = datetime.now().timestamp()
                ts = datetime.fromtimestamp(tmsm).isoformat()
                harian.done = ts
            form.save()
            return redirect('cln_progress')
    else:
        form = dailyForm(instance=harian)
    context = {
        'form': form,
        'harian': harian,
        'tanggal': date.today(),
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_progress_check_single.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_history_check_single(request, harian_id, history_date):
    harian = cln_daily.objects.get(
        id=harian_id, hariIni=history_date)
    if request.method == 'POST':
        form = dailyForm(request.POST or None, instance=harian)
        if form.is_valid():
            form.save(commit=False)
            if harian.kondisi != '' or harian.keterangan != '' or harian.hasilTemuan != '':
                tmsm = datetime.now().timestamp()
                ts = datetime.fromtimestamp(tmsm).isoformat()
                harian.done = ts
            form.save()
            return redirect('cln_history')
    else:
        form = dailyForm(instance=harian)
    context = {
        'form': form,
        'harian': harian,
        'tanggal': cln_latest_history.objects.get(history=history_date),
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_history_check_single.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_progress_check_all(request, area_id):
    areas = cln_area.objects.get(id=area_id)
    subareas = cln_subarea.objects.filter(
        namaAreaSubarea=areas.id)
    dailyFormSet = modelformset_factory(
        cln_daily, form=dailyForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = dailyFormSet(request.POST or None,
                               queryset=cln_daily.objects.filter(hariIni=date.today(), dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
        if formset.is_valid():
            for form in formset:
                harian = form.save(commit=False)
                if harian.kondisi != '' and harian.kondisi != None or harian.keterangan != '' or harian.hasilTemuan != '':
                    tmsm = datetime.now().timestamp()
                    ts = datetime.fromtimestamp(tmsm).isoformat()
                    harian.done = ts
                else:
                    harian.done = None
                harian.save()
            return redirect('cln_progress')
    else:
        formset = dailyFormSet(queryset=cln_daily.objects.filter(
            hariIni=date.today(), dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
    formfull = dict()
    for (subarea, form) in zip(subareas, formset):
        formfull.update({subarea.namaSubarea: form})
    context = {
        'formset': formset,
        'areas': areas,
        'subareas': subareas,
        'tanggal': date.today(),
        'formfull': formfull,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_progress_check_all.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_history_check_all(request, area_id, history_date):
    areas = cln_area.objects.get(id=area_id)
    subareas = cln_subarea.objects.filter(
        namaAreaSubarea=areas.id)
    dailyFormSet = modelformset_factory(
        cln_daily, form=dailyForm, can_delete=False, extra=0)
    try:
        tanggal = datetime.strptime(history_date, '%Y-%m-%d %H:%M:%S')
    except:
        tanggal = datetime.strptime(history_date, '%Y-%m-%d')
    if request.method == "POST":
        formset = dailyFormSet(request.POST or None,
                               queryset=cln_daily.objects.filter(hariIni=tanggal.strftime("%Y-%m-%d"), dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
        if formset.is_valid():
            for form in formset:
                harian = form.save(commit=False)
                if harian.kondisi != '' and harian.kondisi != None or harian.keterangan != '' or harian.hasilTemuan != '':
                    tmsm = datetime.now().timestamp()
                    ts = datetime.fromtimestamp(tmsm).isoformat()
                    harian.done = ts
                else:
                    harian.done = None
                harian.save()
            return redirect('cln_history')
    else:
        formset = dailyFormSet(queryset=cln_daily.objects.filter(
            hariIni=tanggal.strftime("%Y-%m-%d"), dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
    formfull = dict()
    for (subarea, form) in zip(subareas, formset):
        formfull.update({subarea.namaSubarea: form})
    context = {
        'formset': formset,
        'areas': areas,
        'subareas': subareas,
        'formfull': formfull,
        'tanggal': cln_latest_history.objects.get(history=tanggal.strftime("%Y-%m-%d")),
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_history_check_all.html', context)


# @login_required(login_url='user_login')
class cln_history_download_pdf(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        briImage = user_bri_image.objects.get(imageName="logo bri")
        obj = cln_latest_history.objects.get(id=1, isDelete=False)
        history_date = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(obj.history, datetime.min.time()))
        days = cln_day.objects.filter(hariIni=obj.history, isDelete=False)
        areas = cln_area.objects.filter(
            createAt__lte=history_date, deleteAt__gt=history_date)
        subareas = cln_subarea.objects.filter(
            createAt__lte=history_date, deleteAt__gt=history_date)
        dailies = cln_daily.objects.filter(hariIni=obj.history)
        data = {
            'days': days,
            'areas': areas,
            'subareas': subareas,
            'dailies': dailies,
            'tanggal': obj.history,
            'briImage': briImage,
            'title': 'Checklist Kebersihan'
        }
        pdf = render_to_pdf('cleaning/cln_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Checklist_Kebersihan_%s.pdf" % (obj.history)
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response


class cln_progress_download_pdf(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        briImage = user_bri_image.objects.get(imageName="logo bri")

        today_date = pytz.timezone(settings.TIME_ZONE).localize(
            datetime.combine(date.today(), datetime.min.time()))
        days = cln_day.objects.filter(hariIni=date.today(), isDelete=False),
        areas = cln_area.objects.filter(
            createAt__lte=today_date, isDelete=False)
        subareas = cln_subarea.objects.filter(
            createAt__lte=today_date, isDelete=False)
        dailies = cln_daily.objects.filter(
            hariIni=date.today(), isDelete=False)
        data = {
            'days': days,
            'areas': areas,
            'subareas': subareas,
            'dailies': dailies,
            'tanggal': date.today(),
            'briImage': briImage,
            'title': 'Checklist Kebersihan'
        }
        pdf = render_to_pdf('cleaning/cln_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Checklist_Kebersihan_%s.pdf" % (date.today())
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response


@login_required(login_url='user_login')
def cln_history_send_email(request, *args, **kwargs):
    briImage = user_bri_image.objects.get(imageName="logo bri")
    obj = cln_latest_history.objects.get(id=1, isDelete=False)
    history_date = pytz.timezone(settings.TIME_ZONE).localize(
        datetime.combine(obj.history, datetime.min.time()))
    areas = cln_area.objects.filter(
        createAt__lte=obj.history, deleteAt__gt=obj.history)
    subareas = cln_subarea.objects.filter(
        createAt__lte=obj.history, deleteAt__gt=obj.history)
    dailies = cln_daily.objects.filter(hariIni=obj.history)
    context = {
        'days': cln_day.objects.filter(hariIni=obj.history, isDelete=False),
        'areas': areas,
        'subareas': subareas,
        'dailies': dailies,
        'tanggal': obj.history,
        'briImage': briImage,
        'title': 'Checklist Kebersihan'
    }
    html_content = render_to_string('cleaning/cln_pdf_email.html', context)
    text_content = strip_tags(html_content)
    subject = "Checklist_Kebersihan_%s" % (obj.history)
    mail_receiver = settings.EMAIL_HOST_USER  # diganti email sendiri juga bisa
    mail_sender = settings.EMAIL_HOST_USER
    email = EmailMultiAlternatives(
        subject, text_content, mail_sender, [mail_receiver])
    email.attach_alternative(html_content, 'text/html')
    email.attach
    email.send()
    return redirect('cln_history')


@login_required(login_url='user_login')
@maker_only
def cln_default_check_all(request, area_id):
    areas = cln_area.objects.get(id=area_id, isDelete=False)
    subareas = cln_subarea.objects.filter(
        namaAreaSubarea=areas.id, isDelete=False)
    defaultFormSet = modelformset_factory(
        cln_default, form=defaultForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = defaultFormSet(request.POST or None,
                                 queryset=cln_default.objects.filter(defaultSubarea__namaAreaSubarea=areas.id, isDelete=False), prefix='default')
        if formset.is_valid():
            for form in formset:
                default = form.save(commit=False)
                default.save()
            for subarea in subareas:
                defaults = cln_default.objects.filter(defaultSubarea=subarea)
                harians = cln_daily.objects.filter(
                    dailySubarea=subarea, hariIni=date.today(), isDelete=False)
                for harian in harians:
                    for default in defaults:
                        if harian.kondisi == '' or harian.kondisi == None:
                            harian.kondisi = default.defaultKondisi
                        if harian.keterangan == '' or harian.keterangan == None:
                            harian.keterangan = default.defaultKeterangan
                        if harian.hasilTemuan == '' or harian.keterangan == None:
                            harian.hasilTemuan = default.defaultHasilTemuan
                    harian.save()
            return redirect('cln_settings')
    else:
        formset = defaultFormSet(queryset=cln_default.objects.filter(
            defaultSubarea__namaAreaSubarea=areas.id, isDelete=False), prefix='default')
    formfull = dict()
    for (subarea, form) in zip(subareas, formset):
        formfull.update({subarea.namaSubarea: form})
    context = {
        'formset': formset,
        'areas': areas,
        'subareas': subareas,
        'tanggal': date.today(),
        'formfull': formfull,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_default_check_all.html', context)
