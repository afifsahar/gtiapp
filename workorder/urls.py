from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', wo_home, name='wo_home'),
    path('work/detail/day=<day_id>', wo_work_detail, name='wo_work_detail'),
    path('work/add', wo_work_add, name='wo_work_add'),
    path('work/edit/day=<day_id>', wo_work_edit, name='wo_work_edit'),
    path('work/delete/day=<day_id>', wo_work_delete, name='wo_work_delete'),
    path('work/delete/day=<day_id>/confirmed',
         wo_work_delete_confirm, name='wo_work_delete_confirm'),
    path('progress/day=<day_id>', wo_progress_add, name='wo_progress_add'),
    path('download-pdf/day=<day_id>', wo_work_download_pdf.as_view(),
         name='wo_work_download_pdf'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
