
from django.http import HttpResponse
from django.shortcuts import render, redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all().first().name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def maker_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all().first().name
        if group == 'maker':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('401_unauthorized_maker')
    return wrapper_function


def briks_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all().first().name
        if group == 'briks':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('401_unauthorized_maker')
    return wrapper_function


def checker_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all().first().name
        if group == 'checker':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('401_unauthorized_checker')
    return wrapper_function


def signer_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all().first().name
        if group == 'signer':
            return view_func(request, *args, **kwargs)
        else:
            # return HttpResponse('SIGNER Only page')
            return redirect('401_unauthorized_signer')
    return wrapper_function
