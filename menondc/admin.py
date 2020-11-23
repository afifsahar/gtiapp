from django.contrib import admin
from .models import *


class SubareaAdmin(admin.ModelAdmin):
    model = mendc_subarea
    list_display = ('namaSubarea', 'get_area',)
    search_fields = ('namaSubarea', 'get_area', )

    def get_area(self, obj):
        return obj.namaAreaSubarea.namaArea

    get_area.admin_order_field = 'namaAreaSubarea'  # Allows column order sorting
    get_area.short_description = 'Nama Area'  # Renames column head


class DayAdmin(admin.ModelAdmin):
    model = mendc_day
    list_display = ('hariIni', 'mendcMaker', 'mendcChecker', 'mendcSigner',)
    search_fields = ('hariIni', 'mendcMaker', 'mendcChecker', 'mendcSigner',)

    # def get_area(self, obj):
    #     return obj.namaAreaSubarea.namaArea

    # get_area.admin_order_field = 'namaAreaSubarea'  # Allows column order sorting
    # get_area.short_description = 'Nama Area'  # Renames column head


class DailyAdmin(admin.ModelAdmin):
    model = mendc_daily
    list_display = ('hariIni', 'get_area', 'get_subarea',)
    search_fields = ('hariIni', 'get_area', 'get_subarea',)

    def get_area(self, obj):
        return obj.dailySubarea.namaAreaSubarea.namaArea

    get_area.admin_order_field = 'dailySubarea'  # Allows column order sorting
    get_area.short_description = 'Nama Area'  # Renames column head

    def get_subarea(self, obj):
        return obj.dailySubarea.namaSubarea

    get_subarea.admin_order_field = 'dailySubarea'  # Allows column order sorting
    get_subarea.short_description = 'Nama Subarea'  # Renames column head


admin.site.register(mendc_day, DayAdmin)
admin.site.register(mendc_area)
admin.site.register(mendc_subarea, SubareaAdmin)
admin.site.register(mendc_daily, DailyAdmin)
admin.site.register(mendc_latest_history)