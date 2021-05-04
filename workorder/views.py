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
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage


# Create your views here.
@login_required(login_url='user_login')
def wo_home(request):
    wos = wo_workorder.objects.filter(isDelete=False)
    days = wo_day.objects.filter(isDelete=False).order_by('-createAt')
    # descriptions = wo_description.objects.filter(isDelete=False)
    paginator = Paginator(days, 3)
    page_number = request.GET.get('page', 1)
    try:
        pg = paginator.page(page_number)  # get_page or page
    except EmptyPage:
        pg = paginator.page(1)
    context = {
        'dayCount': days.count(),
        'days': pg,
        # 'descriptions': descriptions,
        'wos': wos,
        'title': 'Work Order',
    }
    return render(request, 'workorder/wo_home.html', context)


@login_required(login_url='user_login')
def wo_work_detail(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    descriptions = wo_description.objects.get(
        descriptionDay=days.id, isDelete=False)
    workorders = wo_workorder.objects.get(
        workorderDay=days.id, workorderDescription=descriptions.id, isDelete=False)
    progresss = wo_progress.objects.get(
        progressDay=days.id, progressDescription=descriptions.id, isDelete=False)
    rincians = wo_rincian.objects.filter(
        rincianProgress=progresss.id, isDelete=False)
    context = {
        'days': days,
        'descriptions': descriptions,
        'workorders': workorders,
        'rincians': rincians,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_detail.html', context)


@login_required(login_url='user_login')
@maker_only
def wo_work_add(request):
    if request.method == "POST":
        # a_form = areaForm(request.POST or None)
        # cs_form = csForm(request.POST or None)
        # a_form.is_valid and cs_form.is_valid and
        d_form = descriptionForm(request.POST or None)
        w_form = workorderForm(request.POST or None)
        if d_form.is_valid() and w_form.is_valid():
            day = wo_day.objects.create()
            desc = d_form.save(commit=False)
            desc.descriptionDay = day
            desc.save()
            work = w_form.save(commit=False)
            work.workorderDay = day
            work.workorderDescription = desc
            work.woMaker = request.user
            work.save()
            progress = wo_progress.objects.create(
                progressDay=day,
                progressDescription=desc
            )
            progress.save()
            rinc = wo_rincian(rincianProgress=progress)
            rinc.save()

            return redirect('wo_home')
    else:
        # a_form = areaForm()
        # cs_form = csForm()
        d_form = descriptionForm()
        w_form = workorderForm()
    context = {
        # 'a_form': a_form,
        # 'cs_form': cs_form,
        'd_form': d_form,
        'w_form': w_form,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_add.html', context)


@login_required(login_url='user_login')
@maker_only
def wo_work_edit(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    descriptions = wo_description.objects.get(
        descriptionDay=days.id, isDelete=False)
    workorders = wo_workorder.objects.get(
        workorderDay=days.id, workorderDescription=descriptions.id, isDelete=False)
    if request.method == "POST":
        # wc_form = workorderCreateAtForm(
        #     request.POST or None, instance=workorders)
        d_form = descriptionForm(request.POST or None, instance=descriptions)
        w_form = workorderForm(request.POST or None, instance=workorders)
        if d_form.is_valid() and w_form.is_valid():
            day = days
            desc = d_form.save(commit=False)
            desc.descriptionDay = day
            desc.save()
            work = w_form.save(commit=False)
            work.workorderDay = day
            work.workorderDescription = desc
            if work.woMaker == None or work.woMaker == '':
                work.woMaker = request.user
            work.save()
            # wc = wc_form.save(commit=False)
            # wc.save()
            return redirect('wo_home')
    else:
        # wc_form = workorderCreateAtForm(instance=workorders)
        d_form = descriptionForm(instance=descriptions)
        w_form = workorderForm(instance=workorders)
    context = {
        'd_form': d_form,
        'w_form': w_form,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_edit.html', context)


@login_required(login_url='user_login')
@maker_only
def wo_work_delete(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    context = {
        'days': days,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_delete.html', context)


@login_required(login_url='user_login')
@maker_only
def wo_work_delete_confirm(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    descriptions = wo_description.objects.get(
        descriptionDay=days.id, isDelete=False)
    workorders = wo_workorder.objects.get(
        workorderDay=days.id, workorderDescription=descriptions.id, isDelete=False)
    progresss = wo_progress.objects.get(
        progressDay=days.id, progressDescription=descriptions.id, isDelete=False)
    rincians = wo_rincian.objects.filter(
        rincianProgress=progresss.id, isDelete=False)
    days.isDelete = True
    days.save()
    descriptions.isDelete = True
    descriptions.save()
    workorders.isDelete = True
    workorders.save()
    progresss.isDelete = True
    progresss.save()
    for rincian in rincians:
        rincian.isDelete = True
        rincian.save()
    context = {
        'days': days,
        # 'descriptions': descriptions,
        # 'workorders': workorders,
        # 'rincians': rincians,
        'title': 'Work Order'
    }
    return redirect('wo_home')


@login_required(login_url='user_login')
@briks_only
def wo_progress_add(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    progs = wo_progress.objects.get(progressDay=days, isDelete=False)
    RincianFormSet = modelformset_factory(wo_rincian, form=rincianForm, exclude=(
        'lastUpdate', 'createAt', 'isDelete', 'briksUser', 'ospUser', 'rincianProgress'), can_delete=False, extra=1)
    if request.method == "POST":
        formset = RincianFormSet(request.POST or None,
                                 queryset=wo_rincian.objects.filter(rincianProgress=progs), prefix='rincian')
        if formset.is_valid():
            for f in formset:
                rinc = f.save(commit=False)
                rinc.rincianProgress = progs
                if rinc.briksUser == '' or rinc.briksUser == None:
                    rinc.briksUser = request.user
                rinc.save()
            return redirect('wo_home')
    else:
        formset = RincianFormSet(queryset=wo_rincian.objects.filter(
            rincianProgress=progs), prefix='rincian')
    context = {
        'progs': progs,
        'formset': formset,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_progress_add.html', context)


class wo_work_download_pdf(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        briImage = user_bri_image.objects.get(imageName="logo bri")
        days = wo_day.objects.get(id=self.kwargs['day_id'], isDelete=False)
        descriptions = wo_description.objects.get(
            descriptionDay=days, isDelete=False)
        workorders = wo_workorder.objects.get(
            workorderDay=days, workorderDescription=descriptions.id, isDelete=False)
        progresss = wo_progress.objects.get(
            progressDay=days, progressDescription=descriptions.id, isDelete=False)
        rincians = wo_rincian.objects.filter(
            rincianProgress=progresss, isDelete=False)
        data = {
            'briImage': briImage,
            'days': days,
            'descriptions': descriptions,
            'workorders': workorders,
            'progresss': progresss,
            'rincians': rincians,
        }
        pdf = render_to_pdf('workorder/wo_pdf.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Work_Order_%s.pdf" % (days.createAt)
        content = "inline; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
