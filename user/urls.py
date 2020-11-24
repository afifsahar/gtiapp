from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', user_home, name='user_home'),
    path('login', user_login, name='user_login'),
    path('logout', user_logout, name="user_logout"),
    path('register', user_register, name="user_register"),
    path('profile=<username>', user_profile, name="user_profile"),
    path('profile=<username>/password-change',
         user_profile_password_change, name="user_profile_password_change"),

    path('profile=<username>/edit', user_profile_edit, name="user_profile_edit"),
    # path('profile=<username>/notification',
    #      user_profile_notification, name="user_profile_notification"),

    # path('profile=<username>/notification/check_kebersihan_id=<day_id>_maked',
    #      user_cln_maker_notification, name="user_cln_maker_notification"),
    # path('profile=<username>/notification/perangkat_gedung_id=<day_id>_maked',
    #      user_mendc_maker_notification, name="user_mendc_maker_notification"),

    # path('profile=<username>/notification/check_kebersihan_id=<day_id>_checked',
    #      user_cln_checker_notification, name="user_cln_checker_notification"),
    # path('profile=<username>/notification/perangkat_gedung_id=<day_id>_checked',
    #      user_mendc_checker_notification, name="user_mendc_checker_notification"),

    # path('profile=<username>/notification/check_kebersihan_id=<day_id>_signed',
    #      user_cln_signer_notification, name="user_cln_signer_notification"),
    # path('profile=<username>/notification/perangkat_gedung_id=<day_id>_signed',
    #      user_mendc_signer_notification, name="user_mendc_signer_notification"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/user_password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/user_password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/user_password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/user_password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('401-unauthorized/maker', user_401_unauthorized_maker,
         name='401_unauthorized_maker'),
    path('401-unauthorized/checker', user_401_unauthorized_checker,
         name='401_unauthorized_checker'),
    path('401-unauthorized/signer', user_401_unauthorized_signer,
         name='401_unauthorized_signer'),
    path('404-page-not-found', user_404_page_not_found,
         name='404_page_not_found'),

    path('profile-<username>/configuration',
         user_profile_configuration, name="user_profile_configuration"),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
