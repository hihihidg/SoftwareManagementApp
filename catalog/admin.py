from django.contrib import admin
from .models import RequestingSoftware, Software, SoftwareInstance, SoftwareType
from django.contrib.auth.models import Permission
admin.site.register(Permission)
admin.site.register(Software)
admin.site.register(SoftwareType)
admin.site.register(RequestingSoftware)

@admin.register(SoftwareInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('software', 'user', 'renewal_date', 'id')
    fieldsets = (
        (None, {
            'fields': ('software','id')
        }),
        ('Availability', {
            'fields': ('renewal_date','user')
        }),
    )

