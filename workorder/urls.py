from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', wo_home, name='wo_home'),
    path('work/add', wo_work_add, name='wo_work_add'),
    path('work/edit/day=<day_id>', wo_work_edit, name='wo_work_edit'),
    path('work/delete/day=<day_id>', wo_work_delete, name='wo_work_delete'),
    path('progress/add/day=<day_id>', wo_progress_add, name='wo_progress_add'),
    path('progress/edit/day=<day_id>', wo_progress_edit, name='wo_progress_edit'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
