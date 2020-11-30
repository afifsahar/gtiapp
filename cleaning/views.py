from django.shortcuts import render, redirect
from user.models import user_bri_image
from user.views import user_login
from user.decorators import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.models import *
from django.conf import settings
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from .utils import render_to_pdf
from django.views.generic import View
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from datetime import datetime, date
import datetime
from .forms import *
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .autos import *

@login_required(login_url='user_login')
def cln_home(request):
    context = {
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_home.html', context)


@login_required(login_url='user_login')
def cln_settings(request):
    areas = cln_area.objects.all()
    subareas = cln_subarea.objects.all()
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
    areas = cln_area.objects.get(id=area_id)
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
            cln_when_create_subarea()
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
    areas = cln_area.objects.get(id=area_id)
    subareas = cln_subarea.objects.filter(namaAreaSubarea=areas)
    context = {
        'areas': areas,
        'subareas': subareas,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_area_delete.html', context)


@login_required(login_url='user_login')
@maker_only
def cln_area_delete_confirm(request, area_id):
    areas = cln_area.objects.get(id=area_id)
    areas.delete()
    # context = {
    #     'areas': cln_area.objects.all(),
    #     'title': 'Checklist Kebersihan'
    # }
    return redirect('cln_settings')


@login_required(login_url='user_login')
def cln_progress(request):
    areas = cln_area.objects.all()
    subareas = cln_subarea.objects.all()
    harians = cln_daily.objects.filter(hariIni=date.today())
    areaCount = areas.count()
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': harians,
        'tanggal': date.today(),
        "areaCount": areaCount,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_progress.html', context)


@login_required(login_url='user_login')
def cln_history(request):
    obj = cln_latest_history.objects.get(id=1)
    if request.method == 'POST':
        tgl = request.POST.get('date')
        if tgl:
            obj.history = datetime.strptime(tgl, '%Y-%m-%d').date()
            obj.save()
    areas = cln_area.objects.all()
    subareas = cln_subarea.objects.all()
    dailies = cln_daily.objects.filter(hariIni=obj.history)
    dailies_queryset = dailies.count()
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': dailies,
        'tanggal': obj.history,
        'dailies_queryset': dailies_queryset,
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_history.html', context)

# def cln_area_json(request):
#     areas = cln_area.objects.all()
#     dataArea = [area.to_dict_json() for area in areas]
#     response = {'data': dataArea}
#     return JsonResponse(response)


# def cln_subarea_json(request):
#     subareas = cln_subarea.objects.all()
#     dataSubarea = [subarea.to_dict_json() for subarea in subareas]
#     response = {'data': dataSubarea}
#     return JsonResponse(response)


# def cln_daily_json(request):
#     dailies = cln_daily.objects.filter(hariIni=date.today())
#     dataDaily = [daily.to_dict_json() for daily in dailies]
#     response = {'data': dataDaily}
#     return JsonResponse(response)

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
    harian = cln_daily.objects.get(id=harian_id, hariIni=history_date)
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
    subareas = cln_subarea.objects.filter(namaAreaSubarea=areas.id)
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
    subareas = cln_subarea.objects.filter(namaAreaSubarea=areas.id)
    dailyFormSet = modelformset_factory(
        cln_daily, form=dailyForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = dailyFormSet(request.POST or None,
                               queryset=cln_daily.objects.filter(hariIni=history_date, dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
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
            hariIni=history_date, dailySubarea__namaAreaSubarea=areas.id), prefix='daily')
    formfull = dict()
    for (subarea, form) in zip(subareas, formset):
        formfull.update({subarea.namaSubarea: form})
    context = {
        'formset': formset,
        'areas': areas,
        'subareas': subareas,
        'formfull': formfull,
        'tanggal': cln_latest_history.objects.get(history=history_date),
        'title': 'Checklist Kebersihan'
    }
    return render(request, 'cleaning/cln_history_check_all.html', context)


# @login_required(login_url='user_login')
class cln_history_download_pdf(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        briImage = user_bri_image.objects.get(imageName="logo bri")
        obj = cln_latest_history.objects.get(id=1)
        data = {
            'days': cln_day.objects.filter(hariIni=obj.history),
            'areas': cln_area.objects.all(),
            'subareas': cln_subarea.objects.all(),
            'dailies': cln_daily.objects.filter(hariIni=obj.history),
            'tanggal': obj.history,
            'briImage': briImage,
            'title': 'Checklist Kebersihan'
        }
        pdf = render_to_pdf('cleaning/cln_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Checklist_Kebersihan_%s.pdf" % (obj.history)
        content = "inline; attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response


@login_required(login_url='user_login')
def cln_history_send_email(request, *args, **kwargs):
    briImage = user_bri_image.objects.get(imageName="logo bri")
    obj = cln_latest_history.objects.get(id=1)
    context = {
        'days': cln_day.objects.filter(hariIni=obj.history),
        'areas': cln_area.objects.all(),
        'subareas': cln_subarea.objects.all(),
        'dailies': cln_daily.objects.filter(hariIni=obj.history),
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
    areas = cln_area.objects.get(id=area_id)
    subareas = cln_subarea.objects.filter(namaAreaSubarea=areas.id)
    defaultFormSet = modelformset_factory(
        cln_default, form=defaultForm, can_delete=False, extra=0)
    if request.method == "POST":
        formset = defaultFormSet(request.POST or None,
                                 queryset=cln_default.objects.filter(defaultSubarea__namaAreaSubarea=areas.id), prefix='default')
        if formset.is_valid():
            for form in formset:
                default = form.save(commit=False)
                default.save()
            for subarea in subareas:
                defaults = cln_default.objects.filter(defaultSubarea=subarea)
                harians = cln_daily.objects.filter(dailySubarea=subarea)
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
    return render(request, 'cleaning/cln_default_check_all.html', context)
    
