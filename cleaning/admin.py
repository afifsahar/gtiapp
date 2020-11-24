from django.contrib import admin
from .models import *

admin.site.site_header = 'CheckApp Dashboard'


class SubareaAdmin(admin.ModelAdmin):
    model = cln_subarea
    list_display = ('namaSubarea', 'get_area',)
    search_fields = ('namaSubarea', 'get_area', )

    def get_area(self, obj):
        return obj.namaAreaSubarea.namaArea

    get_area.admin_order_field = 'namaAreaSubarea'  # Allows column order sorting
    get_area.short_description = 'Nama Area'  # Renames column head


class DayAdmin(admin.ModelAdmin):
    model = cln_day
    list_display = ('hariIni', 'clnMaker', 'clnChecker', 'clnSigner',)
    search_fields = ('hariIni', 'clnMaker', 'clnChecker', 'clnSigner',)

    # def get_area(self, obj):
    #     return obj.namaAreaSubarea.namaArea

    # get_area.admin_order_field = 'namaAreaSubarea'  # Allows column order sorting
    # get_area.short_description = 'Nama Area'  # Renames column head


class DailyAdmin(admin.ModelAdmin):
    model = cln_daily
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


admin.site.register(cln_day, DayAdmin)
admin.site.register(cln_area)
admin.site.register(cln_subarea, SubareaAdmin)
admin.site.register(cln_daily, DailyAdmin)
admin.site.register(cln_latest_history)
