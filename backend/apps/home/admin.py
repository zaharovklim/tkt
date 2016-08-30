from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from .models import Widget, Barcode
from import_export import resources
from import_export.admin import ImportMixin


class BarcodeResource(resources.ModelResource):

    class Meta:
        model = Barcode
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'article', 'barcode')

class BarcodeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = BarcodeResource


def get_groups(self, obj):
    return ", ".join([group.name for group in obj.groups.all()])

UserAdmin.get_groups = get_groups
UserAdmin.get_groups.short_description = 'Groups'
UserAdmin.list_display = (
    'username', 'email', 'last_name', 'is_active', 'get_groups', 'is_staff'
)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Widget)
admin.site.register(Barcode, BarcodeAdmin)
