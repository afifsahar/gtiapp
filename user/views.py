from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms_profiles import *
from .forms_users import *
from .forms_passwords import *
from .decorators import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from datetime import datetime, date
from cleaning.models import *
from menondc.models import *
import math
from django.db.models import Q


@login_required(login_url='user_login')
def user_home(request):
    cleaning_works_left = cln_daily.objects.filter(Q(hariIni=date.today()) & Q(kondisi=None)).count()
    menondc_works_left = mendc_daily.objects.filter(Q(hariIni=date.today()) & Q(kondisi='')).count()
    cln_days = None
    mendc_days = None
    if request.user.groups.all().first().name == 'maker':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=True) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True)).count()
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=True) & Q(
            mendcChecker__isnull=True) & Q(mendcSigner__isnull=True)).count()
    if request.user.groups.all().first().name == 'checker':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True)).count()
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=False) & Q(
            mendcChecker__isnull=True) & Q(mendcSigner__isnull=True)).count()
    if request.user.groups.all().first().name == 'signer':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=False) & Q(clnSigner__isnull=True)).count()
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=False) & Q(
            mendcChecker__isnull=False) & Q(mendcSigner__isnull=True)).count()
    days = cln_days + mendc_days
    context = {
        'tanggal': date.today(),
        'cleaning_works_done': cleaning_works_left,
        'menondc_works_done': menondc_works_left,
        'days':days,
    }
    return render(request, 'user/user_home.html', context)


@ unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        next = request.GET.get('next')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = authenticate(username=username, password=password)
                messages.success(request, 'Verifikasi berhasil')
                auth_login(request, user)
                if next:
                    return redirect(next)
                messages.success(request, 'Verifikasi Berhasil.')
                return redirect('user_home')
            except auth.ObjectDoesNotExist:
                return HttpResponse("Log in Failed. Try Again")
        else:
            messages.warning(request, 'Verifikasi Gagal')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'user/user_login.html', context)


@ login_required(login_url='user_login')
def user_logout(request):
    auth_logout(request)
    messages.success(request, 'Anda Berhasil Keluar Sesi')
    return redirect('user_login')


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        gform = GroupForm(request.POST or None)
        if form.is_valid() and gform.is_valid:
            guser = gform.save(commit=False)
            name = gform.cleaned_data.get('name')
            user = form.save(commit=False)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.save()
            user.groups.set(name)
            user.set_password(password)
            user.save()
            messages.success(request, 'Akun' + ' ' + first_name +
                             ' ' + last_name + ' ' + 'telah berhasil dibuat')
            return redirect('user_login')
        else:
            messages.warning(request, 'Kesalahan. Coba Lagi')

    else:
        form = UserRegistrationForm()
        gform = GroupForm()
    context = {
        'form': form,
        'gform': gform,
    }
    return render(request, 'user/user_register.html', context)


@ login_required(login_url='user_login')
def user_profile(request, username):
    return render(request, 'user/user_profile.html')


@ login_required(login_url='user_login')
def user_profile_password_change(request, username):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_profile', username=request.user.username)
    else:
        form = PasswordChangeForm(data=request.POST, user=request.user)

    context = {'form': form}
    return render(request, 'user/user_profile_password_change.html', context)


@ login_required(login_url='user_login')
def user_profile_edit(request, username):
    if request.method == 'POST':
        p_form = UserProfileForm(request.POST or None,
                                 user=request.user, instance=request.user)
        pp_form = UserProfilePhotoForm(
            request.POST or None, request.FILES or None, instance=request.user.userProfile)
        if p_form.is_valid() and pp_form.is_valid():
            p_form.save()
            pp_form.save()
            messages.success(
                request, 'Profil pengguna telah berhasil diperbaharui')
            return redirect('user_profile', username=request.user.username)
        else:
            messages.error(request, 'Profile pengguna gagal diperbaharui')
    else:
        p_form = UserProfileForm(
            user=request.user, instance=request.user)
        pp_form = UserProfilePhotoForm(instance=request.user.userProfile)
    context = {
        'p_form': p_form,
        'pp_form': pp_form,
    }
    return render(request, 'user/user_profile_edit.html', context)


@ login_required(login_url='user_login')
def user_profile_notification(request, username):
    cln_days = None
    mendc_days = None
    if request.user.groups.all().first().name == 'maker':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=True) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True))[:5]
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=True) & Q(
            mendcChecker__isnull=True) & Q(mendcSigner__isnull=True))[:5]
    if request.user.groups.all().first().name == 'checker':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=True) & Q(clnSigner__isnull=True))[:5]
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=False) & Q(
            mendcChecker__isnull=True) & Q(mendcSigner__isnull=True))[:5]
    if request.user.groups.all().first().name == 'signer':
        cln_days = cln_day.objects.filter(Q(clnMaker__isnull=False) & Q(
            clnChecker__isnull=False) & Q(clnSigner__isnull=True))[:5]
        mendc_days = mendc_day.objects.filter(Q(mendcMaker__isnull=False) & Q(
            mendcChecker__isnull=False) & Q(mendcSigner__isnull=True))[:5]
    context = {
        'cln_days': cln_days,
        'mendc_days': mendc_days,
    }
    return render(request, 'user/user_profile_notification.html', context)


@ login_required(login_url='user_login')
def user_cln_maker_notification(request, username, day_id, day_date):
    cln_days = None
    if request.user.groups.all().first().name == 'maker':
        cln_days = cln_day.objects.get(id=day_id, hariIni=day_date)
        cln_days.clnMaker = User.objects.get(username=request.user.username)
        cln_days.save()

    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_mendc_maker_notification(request, username, day_id, day_date):
    mendc_days = None
    if request.user.groups.all().first().name == 'maker':
        mendc_days = mendc_day.objects.get(id=day_id, hariIni=day_date)
        mendc_days.mendcMaker = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_cln_checker_notification(request, username, day_id, day_date):
    cln_days = None
    if request.user.groups.all().first().name == 'checker':
        cln_days = cln_day.objects.get(id=day_id, hariIni=day_date)
        cln_days.clnChecker = User.objects.get(username=request.user.username)
        cln_days.save()

    return redirect('user_profile_notification', username=request.user.username)

@ login_required(login_url='user_login')
def user_mendc_checker_notification(request, username, day_id, day_date):
    mendc_days = None
    if request.user.groups.all().first().name == 'checker':
        mendc_days = mendc_day.objects.get(id=day_id, hariIni=day_date)
        mendc_days.mendcChecker = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_cln_signer_notification(request, username, day_id, day_date):
    cln_days = None
    if request.user.groups.all().first().name == 'signer':
        cln_days = cln_day.objects.get(id=day_id, hariIni=day_date)
        cln_days.clnSigner = User.objects.get(username=request.user.username)
        cln_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_mendc_signer_notification(request, username, day_id, day_date):
    mendc_days = None
    if request.user.groups.all().first().name == 'signer':
        mendc_days = mendc_day.objects.get(id=day_id, hariIni=day_date)
        mendc_days.mendcSigner = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)

@ login_required(login_url='user_login')
def user_cln_notification_seefile(request, username, day_id, day_date):
    areas = cln_area.objects.all()
    subareas = cln_subarea.objects.all()
    dailies = cln_daily.objects.filter(hariIni=day_date)
    days = cln_day.objects.filter(id=day_id)
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': dailies,
        'days':days,
    }
    return render(request,'user/user_cln_notification_seefile.html',context)

@ login_required(login_url='user_login')
def user_mendc_notification_seefile(request, username, day_id, day_date):
    areas = mendc_area.objects.all()
    subareas = mendc_subarea.objects.all()
    dailies = mendc_daily.objects.filter(hariIni=day_date)
    days = mendc_day.objects.filter(id=day_id)
    context = {
        'areas': areas,
        'subareas': subareas,
        'harians': dailies,
        'days':days,
    }
    return render(request,'user/user_mendc_notification_seefile.html',context)




@ login_required(login_url='user_login')
def user_profile_configuration(request, username):
    return redirect('404_page_not_found')

def user_401_unauthorized_maker(request):
    return render(request, 'user/user_401_unauthorized_maker.html')


def user_401_unauthorized_signer(request):
    return render(request, 'user/user_401_unauthorized_signer.html')


def user_401_unauthorized_checker(request):
    return render(request, 'user/user_401_unauthorized_checker.html')


def user_404_page_not_found(request):
    return render(request, 'user/user_404_page_not_found.html')
