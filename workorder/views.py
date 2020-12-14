from django.shortcuts import render, redirect
from .models import *
from .forms import *


# Create your views here.

def wo_home(request):
    days = wo_day.objects.filter(isDelete=False)
    descriptions = wo_description.objects.filter(isDelete=False)
    context = {
        'dayCount':days.count(),
        'days':days,
        'descriptions':descriptions,
        'title': 'Work Order',
    }
    return render(request, 'workorder/wo_home.html',context)

def wo_work_seefile(request, day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    descriptions = wo_description.objects.get(descriptionDay=days.id, isDelete=False)
    workorders = wo_workorder.objects.get(workorderDay=days.id, workorderDescription=descriptions.id, isDelete=False)
    progresss = wo_progress.objects.get(progressDay=days.id, progressDescription=descriptions.id, isDelete=False)
    rincians = wo_rincian.objects.get(rincianProgress=progresss.id, isDelete=False)
    context = {
        'days':days,
        'descriptions':descriptions,
        'workorders':workorders,
        'rincians':rincians,
        'title':'Work Order'
    }
    return render(request, 'workorder/wo_work_seefile.html',context)


# @login_required(login_url='user_login')
# @maker_only
def wo_work_add(request):
    if request.method == "POST":
        c_form = choiceForm(request.POST or None)
        d_form = descriptionForm(request.POST or None)
        w_form = workorderForm(request.POST or None)
        if c_form.is_valid and d_form.is_valid() and w_form.is_valid():
            day = wo_day.objects.create()
            desc = d_form.save(commit=False)
            desc.descriptionDay = day
            # desc.woUser =  None
            desc.save()
            cho = c_form.save(commit=False)
            cho.save()
            work = w_form.save(commit=False)
            work.workorderDay = day
            work.workorderDescription = desc
            work.woMaker = request.user
            work.save()
            progress = wo_progress.objects.create(
                progressDay = day,
                progressDescription = desc
            )
            progress.save()
            rinc = wo_rincian(rincianProgress=progress)
            rinc.save()
            # messages.success(
            #     request, 'New Area in Checklist Kebersihan Successfully Added')
            return redirect('wo_home')
    else:
        c_form = choiceForm()
        d_form = descriptionForm()
        w_form = workorderForm()
    context = {
        'c_form': c_form,
        'd_form': d_form,
        'w_form': w_form,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_add.html', context)

def wo_work_edit(request, day_id):
    days = wo_day.objects.get(id=day_id)
    descriptions = wo_description.objects.get(descriptionDay=days.id)
    workorders = wo_workorder.objects.get(workorderDay=days.id, workorderDescription=descriptions.id)
    if request.method == "POST":
        d_form = descriptionForm(request.POST or None, instance=descriptions)
        w_form = workorderForm(request.POST or None, instance=workorders)
        if d_form.is_valid() and w_form.is_valid():
            day = days
            desc = d_form.save(commit=False)
            desc.descriptionDay = day
            # desc.woUser =  None
            desc.save()
            work = w_form.save(commit=False)
            work.workorderDay = day
            work.workorderDescription = desc
            work.woMaker = request.user
            work.save()
            progress = wo_progress.objects.create(
                progressDay = day,
                progressDescription = desc
            )
            progress.save()
            rinc = wo_rincian(rincianProgress=progress)
            rinc.save()
            # messages.success(
            #     request, 'New Area in Checklist Kebersihan Successfully Added')
            return redirect('wo_home')
    else:
        d_form = descriptionForm(instance=descriptions)
        w_form = workorderForm(instance=workorders)
    context = {
        'd_form': d_form,
        'w_form': w_form,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_work_edit.html', context)

def wo_work_delete(request,day_id):
    days = wo_day.objects.get(id=day_id, isDelete=False)
    descriptions = wo_description.objects.get(descriptionDay=days.id, isDelete=False)
    workorders = wo_workorder.objects.get(workorderDay=days.id, workorderDescription=descriptions.id, isDelete=False)
    progresss = wo_progress.objects.get(progressDay=days.id, progressDescription=descriptions.id, isDelete=False)
    rincians = wo_rincian.objects.get(rincianProgress=progresss.id, isDelete=False)
    days.is_delete = True
    descriptions.is_delete = True
    workorders.is_delete = True
    progresss.is_delete = True
    rincians.is_delete = True
    context = {
        'days':days,
        'descriptions':descriptions,
        'workorders':workorders,
        'rincians':rincians,
        'title':'Work Order'
    }
    return redirect('wo_home')

# @login_required(login_url='user_login')
# @maker_only
def wo_progress_add(request, day_id):
    progresss = wo_progress.objects.get(progressDay=day_id, isDelete=False)
    RincianFormSet = modelformset_factory(wo_rincian, form=rincianForm, exclude=(
        'lastUpdate','createAt','isDelete','briksUser','ospUser','rincianProgress'), can_delete=False, extra=1)
    if request.method == "POST":
        formset = RincianFormSet(request.POST or None,
                                 queryset=wo_rincian.objects.none(), prefix='rincian')
        if formset.is_valid():
            for f in formset:
                rinc = f.save(commit=False)
                rinc.rincianProgress= progresss
                rinc.save()
            # messages.success(
            #     request, 'New Area in Checklist Kebersihan Successfully Added')
            return redirect('wo_home')
    else:
        # messages.warning(
        #     request, 'New Area FAILED to be Added')
        formset = RincianFormSet(queryset=wo_rincian.objects.none(), prefix='rincian')
    context = {
        'formset': formset,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_progress_add.html', context)

def wo_progress_edit(request, day_id):
    progresss = wo_progress.objects.get(progressDay=day_id, isDelete=False)
    RincianFormSet = modelformset_factory(wo_rincian, form=rincianForm, exclude=(
        'lastUpdate','createAt','isDelete','briksUser','ospUser','rincianProgress'), can_delete=False, extra=1)
    if request.method == "POST":
        formset = RincianFormSet(request.POST or None,
                                 queryset=wo_rincian.objects.filter(rincianProgress=progress.id), prefix='rincian')
        if formset.is_valid():
            for f in formset:
                rinc = f.save(commit=False)
                rinc.rincianProgress= progresss
                rinc.save()
            # messages.success(
            #     request, 'New Area in Checklist Kebersihan Successfully Added')
            return redirect('wo_home')
    else:
        # messages.warning(
        #     request, 'New Area FAILED to be Added')
        formset = RincianFormSet(queryset=wo_rincian.objects.filter(rincianProgress=progress.id), prefix='rincian')
    context = {
        'formset': formset,
        'title': 'Work Order'
    }
    return render(request, 'workorder/wo_progress_add.html', context)
