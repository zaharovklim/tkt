from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from apps.tickets.models import Ticket
from apps.tickets.admin import TicketForm
from import_export import resources
from import_export.admin import ImportMixin

from .models import Widget, Barcode


def get_groups(self, obj):
    return ", ".join([group.name for group in obj.groups.all()])

UserAdmin.get_groups = get_groups
UserAdmin.get_groups.short_description = 'Groups'
UserAdmin.list_display = (
    'username', 'email', 'last_name', 'is_active', 'get_groups', 'is_staff'
)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class TicketInline(admin.StackedInline):

    model = Ticket
    form = TicketForm
    extra = 1
    readonly_fields = ('pdf_link', )


class WidgetForm(forms.ModelForm):

    name = forms.CharField()
    internal_name = forms.CharField()

    class Meta:
        model = Widget
        fields = ('name', 'internal_name', 'enabled', )


class BarcodeResource(resources.ModelResource):

    class Meta:
        model = Barcode
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'article', 'barcode')

class BarcodeAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = BarcodeResource


class WidgetAdmin(admin.ModelAdmin):

    form = WidgetForm

    inlines = [
        TicketInline,
    ]

admin.site.register(Widget, WidgetAdmin)
admin.site.register(Barcode, BarcodeAdmin)
