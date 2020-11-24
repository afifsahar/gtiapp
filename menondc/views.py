
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from .forms import *
import datetime
from datetime import datetime, date
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import *
from user.views import user_login
from user.models import user_bri_image
# Create your views here.
from django.views.generic import View
from .utils import render_to_pdf


@login_required(login_url='user_login')
def mendc_home(request):
    context = {
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_home.html', context)


@login_required(login_url='user_login')
def mendc_settings(request):
    areas = mendc_area.objects.all()
    subareas = mendc_subarea.objects.all()
    context = {
        "areas": areas,
        "subareas": subareas,
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_settings.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_area_add(request):
    SubareaFormSet = modelformset_factory(mendc_subarea, form=subareaForm, exclude=(
        'namaAreaSubarea',), can_delete=False, extra=1)
    if request.method == "POST":
        formset = SubareaFormSet(request.POST or None,
                                 queryset=mendc_subarea.objects.none(), prefix='subarea')
        form = areaForm(request.POST or None)
        if formset.is_valid() and form.is_valid():
            areas = form.save(commit=False)
            areas.save()
            for f in formset:
                subareas = f.save(commit=False)
                subareas.namaAreaSubarea = areas
                subareas.save()
            return redirect('mendc_settings')
    else:
        formset = SubareaFormSet(
            queryset=mendc_subarea.objects.none(), prefix='subarea')
        form = areaForm()
    context = {
        'form': form,
        'formset': formset,
        'title': 'Monitoring Gedung'

    }
    return render(request, 'menondc/mendc_area_add.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_area_edit(request, area_id):
    areas = mendc_area.objects.get(id=area_id)
    SubareaFormSet = modelformset_factory(mendc_subarea, form=subareaForm, exclude=(
        'namaAreaSubarea',), can_delete=False, extra=0)
    if request.method == "POST":
        formset = SubareaFormSet(request.POST,
                                 queryset=mendc_subarea.objects.filter(namaAreaSubarea=areas.id), prefix='subarea')
        form = areaForm(request.POST, instance=areas)
        if formset.is_valid() and form.is_valid():
            ar = form.save(commit=False)
            ar.save()
            for f in formset:
                subar = f.save(commit=False)
                subar.namaAreaSubarea = ar
                subar.save()
            return redirect('mendc_settings')
    else:
        formset = SubareaFormSet(queryset=mendc_subarea.objects.filter(
            namaAreaSubarea=areas.id), prefix='subarea')
        form = areaForm(instance=areas)
    context = {
        'form': form,
        'formset': formset,
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_area_edit.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_area_delete(request, area_id):
    areas = mendc_area.objects.get(id=area_id)
    subareas = mendc_subarea.objects.filter(namaAreaSubarea=areas)
    context = {
        'areas': areas,
        'subareas': subareas,
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_area_delete.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_area_delete_confirm(request, area_id):
    areas = mendc_area.objects.get(id=area_id)
    areas.delete()
    # context = {
    #     'areas': mendc_area.objects.all(),
    #     'subareas': mendc_subarea.objects.all(),
    #     'title': 'Monitoring Gedung'
    # }
    return redirect('mendc_settings')


@login_required(login_url='user_login')
def mendc_progress(request):
    areas = mendc_area.objects.all()
    subareas = mendc_subarea.objects.all()
    harians = mendc_daily.objects.filter(hariIni=date.today())
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': harians,
        'tanggal': date.today(),
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_progress.html', context)


@login_required(login_url='user_login')
def mendc_history(request):
    obj = mendc_latest_history.objects.get(id=1)
    if request.method == 'POST':
        tgl = request.POST.get('date')
        if tgl:
            obj.history = datetime.strptime(tgl, '%Y-%m-%d').date()
            obj.save()
    areas = mendc_area.objects.all()
    subareas = mendc_subarea.objects.all()
    dailies = mendc_daily.objects.filter(hariIni=obj.history)
    dailies_queryset = dailies.count()
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': dailies,
        'tanggal': obj.history,
        'dailies_queryset': dailies_queryset,
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_history.html', context)

# def mendc_area_json(request):
#     areas = mendc_area.objects.all()
#     dataArea = [area.to_dict_json() for area in areas]
#     response = {'data': dataArea}
#     return JsonResponse(response)


# def mendc_subarea_json(request):
#     subareas = mendc_subarea.objects.all()
#     dataSubarea = [subarea.to_dict_json() for subarea in subareas]
#     response = {'data': dataSubarea}
#     return JsonResponse(response)


# def mendc_daily_json(request):
#     dailies = mendc_daily.objects.filter(hariIni=date.today())
#     dataDaily = [daily.to_dict_json() for daily in dailies]
#     response = {'data': dataDaily}
#     return JsonResponse(response)

@login_required(login_url='user_login')
@maker_only
def mendc_progress_check_single(request, harian_id):
    harian = mendc_daily.objects.get(id=harian_id)
    if request.method == 'POST':
        form = dailyForm(request.POST or None, instance=harian)
        if form.is_valid():
            form.save(commit=False)
            if harian.kondisi != '' or harian.keterangan != '' or harian.hasilTemuan != '':
                tmsm = datetime.now().timestamp()
                ts = datetime.fromtimestamp(tmsm).isoformat()
                harian.done = ts
            form.save()
            return redirect('mendc_progress')
    else:
        form = dailyForm(instance=harian)
    context = {
        'form': form,
        'harian': harian,
        'tanggal': date.today(),
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_progress_check_single.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_history_check_single(request, harian_id, history_date):
    harian = mendc_daily.objects.get(id=harian_id, hariIni=history_date)
    if request.method == 'POST':
        form = dailyForm(request.POST or None, instance=harian)
        if form.is_valid():
            form.save(commit=False)
            if harian.kondisi != '' or harian.keterangan != '' or harian.hasilTemuan != '':
                tmsm = datetime.now().timestamp()
                ts = datetime.fromtimestamp(tmsm).isoformat()
                harian.done = ts
            form.save()
            return redirect('mendc_history')
    else:
        form = dailyForm(instance=harian)
    context = {
        'form': form,
        'harian': harian,
        'tanggal': mendc_latest_history.objects.get(history=history_date),
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_history_check_single.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_progress_check_all(request, area_id):
    areas = mendc_area.objects.get(id=area_id)
    subareas = mendc_subarea.objects.filter(namaAreaSubarea=areas.id)
    dailyFormSet = modelformset_factory(
        mendc_daily, form=dailyForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = dailyFormSet(request.POST or None,
                               queryset=mendc_daily.objects.filter(hariIni=date.today(), dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
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
            return redirect('mendc_progress')
    else:
        formset = dailyFormSet(queryset=mendc_daily.objects.filter(
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
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_progress_check_all.html', context)


@login_required(login_url='user_login')
@maker_only
def mendc_history_check_all(request, area_id, history_date):
    areas = mendc_area.objects.get(id=area_id)
    subareas = mendc_subarea.objects.filter(namaAreaSubarea=areas.id)
    dailyFormSet = modelformset_factory(
        mendc_daily, form=dailyForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = dailyFormSet(request.POST or None,
                               queryset=mendc_daily.objects.filter(hariIni=history_date, dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
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
            return redirect('mendc_history')
    else:
        formset = dailyFormSet(queryset=mendc_daily.objects.filter(
            hariIni=history_date, dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
    formfull = dict()
    for (subarea, form) in zip(subareas, formset):
        formfull.update({subarea.namaSubarea: form})
    context = {
        'formset': formset,
        'areas': areas,
        'subareas': subareas,
        'formfull': formfull,
        'tanggal': mendc_latest_history.objects.get(history=history_date),
        'title': 'Monitoring Gedung'
    }
    return render(request, 'menondc/mendc_history_check_all.html', context)


# @login_required(login_url='user_login')
class mendc_history_download_pdf(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        briImage = user_bri_image.objects.get(imageName="logo bri")
        obj = mendc_latest_history.objects.get(id=1)
        data = {
            'days': mendc_day.objects.filter(hariIni=obj.history),
            'areas': mendc_area.objects.all(),
            'subareas': mendc_subarea.objects.all(),
            'dailies': mendc_daily.objects.filter(hariIni=obj.history),
            'tanggal': obj.history,
            'briImage': briImage,
            'title': 'Monitoring Gedung'
            # 'user': request.user.first_name+' '+request.user.last_name
        }
        pdf = render_to_pdf('menondc/mendc_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Monitoring_Gedung_%s.pdf" % (obj.history)
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


@login_required(login_url='user_login')
def mendc_history_send_email(request):
    briImage = user_bri_image.objects.get(imageName="logo bri")
    obj = mendc_latest_history.objects.get(id=1)
    context = {
        'days': mendc_day.objects.filter(hariIni=obj.history),
        'areas': mendc_area.objects.all(),
        'subareas': mendc_subarea.objects.all(),
        'dailies': mendc_daily.objects.filter(hariIni=obj.history),
        'tanggal': obj.history,
        'briImage': briImage,
        'title': 'Monitoring Gedung'
    }
    html_content = render_to_string('cleaning/cln_pdf_email.html', context)
    text_content = strip_tags(html_content)
    subject = "Monitoring_Gedung_%s" % (obj.history)
    mail_receiver = "anofian94@gmail.com"
    mail_sender = settings.EMAIL_HOST_USER
    email = EmailMultiAlternatives(
        subject, text_content, mail_sender, [mail_receiver])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return redirect('mendc_history')


@login_required(login_url='user_login')
@maker_only
def mendc_default_check_all(request, area_id):
    areas = mendc_area.objects.get(id=area_id)
    subareas = mendc_subarea.objects.filter(namaAreaSubarea=areas.id)
    defaultFormSet = modelformset_factory(
        mendc_default, form=defaultForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = defaultFormSet(request.POST or None,
                                 queryset=mendc_default.objects.filter(defaultSubarea__namaAreaSubarea=areas.id), prefix='default')
        if formset.is_valid():
            for form in formset:
                default = form.save(commit=False)
                default.save()
            for subarea in subareas:
                defaults = mendc_default.objects.filter(
                    defaultSubarea=subarea, defaultSubarea__namaAreaSubarea=areas.id)
                harians = mendc_daily.objects.filter(
                    dailySubarea=subarea, dailySubarea__namaAreaSubarea=areas.id)
                for (harian, default) in zip(harians, defaults):
                    harian.hariIni = datetime(
                        date.today().year, date.today().month, date.today().day)  # time 00:00:00
                    harian.kondisi = default.defaultKondisi
                    harian.keterangan = default.defaultKeterangan
                    harian.hasilTemuan = default.defaultHasilTemuan
                    harian.save()
            return redirect('mendc_settings')
    else:
        formset = defaultFormSet(queryset=mendc_default.objects.filter(
            defaultSubarea__namaAreaSubarea=areas.id), prefix='default')
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
    return render(request, 'menondc/mendc_default_check_all.html', context)
