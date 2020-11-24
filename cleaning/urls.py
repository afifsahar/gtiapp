from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', cln_home, name='cln_home'),
    path('settings', cln_settings, name='cln_settings'),
    path('settings/area-add', cln_area_add, name='cln_area_add'),
    path('settings/area-edit/area-<area_id>',
         cln_area_edit, name='cln_area_edit'),
    path('settings/area-delete/area-<area_id>',
         cln_area_delete, name='cln_area_delete'),
    path('settings/area-delete/area-<area_id>/confirmed',
         cln_area_delete_confirm, name='cln_area_delete_confirm'),
    path('settings/default-check/area-<area_id>',
         cln_default_check_all, name='cln_default_check_all'),
    path('progress', cln_progress, name='cln_progress'),
    path('progress/subarea-check/harian-<harian_id>',
         cln_progress_check_single, name='cln_progress_check_single'),
    path('progress/subarea-check/area-<area_id>',
         cln_progress_check_all, name='cln_progress_check_all'),
    path('history', cln_history, name='cln_history'),
    path('history/subarea-check/harian-<harian_id>/<history_date>',
         cln_history_check_single, name='cln_history_check_single'),
    path('history/subarea-check/area-<area_id>/<history_date>',
         cln_history_check_all, name='cln_history_check_all'),
    path('history/download-pdf', cln_history_download_pdf.as_view(),
         name='cln_history_download_pdf'),
    path('history/send-email', cln_history_send_email,
         name='cln_history_send_email'),
    #     path('json/area/', cln_area_json, name='cln_area_json'),
    #     path('json/subarea/', cln_subarea_json, name='cln_subarea_json'),
    #     path('json/daily/', cln_daily_json, name='cln_daily_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
