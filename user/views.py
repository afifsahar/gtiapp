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
    cleaning_daily = cln_daily.objects.filter(hariIni=date.today())
    menondc_daily = mendc_daily.objects.filter(hariIni=date.today())
    cleaning_area = cln_area.objects.all().count()
    menondc_area = mendc_area.objects.all().count()

    cleaning_works_done = cleaning_daily.exclude(kondisi='').count(
    )+cleaning_daily.exclude(keterangan='').count()

    menondc_works_done = menondc_daily.exclude(kondisi='').count(
    )+menondc_daily.exclude(keterangan='').count()

    cleaning_works_percent = cleaning_daily.exclude(kondisi='', keterangan='').count()
    menondc_works_percent = menondc_daily.exclude(kondisi='', keterangan='').count()

    # if cleaning_daily.count() != 0:
    #     # cleaning_works_percent = math.ceil(cleaning_daily.exclude(
    #     #     kondisi='', keterangan='', hasilTemuan='').count()/(cleaning_daily.count())*100)
    #     cleaning_works_percent = math.ceil(cleaning_daily.exclude(
    #         kondisi='', keterangan='', hasilTemuan='').count())
    # else:
    #     cleaning_works_percent = 0
    # if menondc_daily.count() != 0:
    #     # menondc_works_percent = math.ceil(menondc_daily.exclude(
    #     #     kondisi='', keterangan='', hasilTemuan='').count()/(menondc_daily.count())*100)
    #     menondc_works_percent = math.ceil(menondc_daily.exclude(kondisi='', keterangan='', hasilTemuan='').count())
    # else:
    #     menondc_works_percent = 0
    context = {
        'tanggal': date.today(),
        'cleaning_daily_count': cleaning_daily.count()*3,
        'menondc_daily_count': menondc_daily.count()*3,
        'cleaning_area_count': cleaning_area,
        'menondc_area_count': menondc_area,
        'cleaning_works_done': cleaning_works_done,
        'menondc_works_done': menondc_works_done,
        'cleaning_works_percent': cleaning_works_percent,
        'menondc_works_percent': menondc_works_percent,
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
def user_cln_maker_notification(request, username, day_id):
    cln_days = None
    if request.user.groups.all().first().name == 'maker':
        cln_days = cln_day.objects.get(id=day_id)
        cln_days.clnMaker = User.objects.get(username=request.user.username)
        cln_days.save()

    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_mendc_maker_notification(request, username, day_id):
    mendc_days = None
    if request.user.groups.all().first().name == 'maker':
        mendc_days = mendc_day.objects.get(id=day_id)
        mendc_days.mendcMaker = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_cln_checker_notification(request, username, day_id):
    cln_days = None
    if request.user.groups.all().first().name == 'checker':
        cln_days = cln_day.objects.get(id=day_id)
        cln_days.clnChecker = User.objects.get(username=request.user.username)
        cln_days.save()

    return redirect('user_profile_notification', username=request.user.username)

@ login_required(login_url='user_login')
def user_mendc_checker_notification(request, username, day_id):
    mendc_days = None
    if request.user.groups.all().first().name == 'checker':
        mendc_days = mendc_day.objects.get(id=day_id)
        mendc_days.mendcChecker = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_cln_signer_notification(request, username, day_id):
    cln_days = None
    if request.user.groups.all().first().name == 'signer':
        cln_days = cln_day.objects.get(id=day_id)
        cln_days.clnSigner = User.objects.get(username=request.user.username)
        cln_days.save()
    return redirect('user_profile_notification', username=request.user.username)


@ login_required(login_url='user_login')
def user_mendc_signer_notification(request, username, day_id):
    mendc_days = None
    if request.user.groups.all().first().name == 'signer':
        mendc_days = mendc_day.objects.get(id=day_id)
        mendc_days.mendcSigner = User.objects.get(
            username=request.user.username)
        mendc_days.save()
    return redirect('user_profile_notification', username=request.user.username)

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
