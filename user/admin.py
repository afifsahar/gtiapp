from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class userAdmin(UserAdmin):
    list_display = ('username', 'first_name',  'email',
                    'is_active', 'is_staff',)
    search_fields = ('username', 'first_name',  'email',)
    # readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class profileAdmin(admin.ModelAdmin):
    model = user_profile
    list_display = ('userProfile', 'get_user_first_name',)
    search_fields = ('userProfile', 'get_user_first_name',)
    # readonly_fields=('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    def get_user_first_name(self, obj):
        return obj.userProfile.first_name

    # Allows column order sorting
    get_user_first_name.admin_order_field = 'userProfile'
    get_user_first_name.short_description = 'First Name'  # Renames column head


admin.site.register(User, userAdmin)
admin.site.register(user_profile, profileAdmin)
admin.site.register(user_bri_image)