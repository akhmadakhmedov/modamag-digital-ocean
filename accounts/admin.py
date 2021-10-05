from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, forgotPassword, UserProfile
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ('name', 'phone_number', 'last_login', 'date_joined')
    list_display_links = ('name', 'phone_number')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class forgotPasswordAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'name']

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
        thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state')

admin.site.register(Account, AccountAdmin)
admin.site.register(forgotPassword, forgotPasswordAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
