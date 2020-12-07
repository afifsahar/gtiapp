from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', mendc_home, name='mendc_home'),
    path('settings', mendc_settings, name='mendc_settings'),
    path('settings/area-add', mendc_area_add, name='mendc_area_add'),
    path('settings/area-edit/area-<area_id>',
         mendc_area_edit, name='mendc_area_edit'),
    path('settings/area-delete/area-<area_id>',
         mendc_area_delete, name='mendc_area_delete'),
    path('settings/area-delete/area-<area_id>/confirmed',
         mendc_area_delete_confirm, name='mendc_area_delete_confirm'),
    path('settings/default-check/area-<area_id>',
         mendc_default_check_all, name='mendc_default_check_all'),
    path('progress', mendc_progress, name='mendc_progress'),
    path('progress/subarea-check/harian-<harian_id>',
         mendc_progress_check_single, name='mendc_progress_check_single'),
    path('progress/subarea-check/area-<area_id>',
         mendc_progress_check_all, name='mendc_progress_check_all'),
    path('history', mendc_history, name='mendc_history'),
    path('history/subarea-check/harian-<harian_id>/<history_date>',
         mendc_history_check_single, name='mendc_history_check_single'),
    path('history/subarea-check/area-<area_id>/<history_date>',
         mendc_history_check_all, name='mendc_history_check_all'),
    path('history/download_pdf', mendc_history_download_pdf.as_view(),
         name='mendc_history_download_pdf'),
    path('progress/download_pdf', mendc_progress_download_pdf.as_view(),
         name='mendc_progress_download_pdf'),
    path('history/send-email', mendc_history_send_email,
         name='mendc_history_send_email'),
    #    path('json/area/', mendc_area_json, name='mendc_area_json'),
    #    path('json/subarea/', mendc_subarea_json, name='mendc_subarea_json'),
    #    path('json/daily/', mendc_daily_json, name='mendc_daily_json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
