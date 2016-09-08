from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportMixin
from image_cropping import ImageCroppingMixin

from apps.tickets.models import Ticket
from apps.tickets.admin import TicketForm
from .models import Widget, Barcode, TicketImage, BarcodeImage, Bidder


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
        fields = ('name', 'internal_name', 'enabled', 'created_by', 'status', 'widget_type', )


class BarcodeResource(resources.ModelResource):

    class Meta:
        model = Barcode
        skip_unchanged = True
        report_skipped = True
        fields = ('id', 'article', 'barcode', 'created_by')

    def before_import(self, dataset, *args, **kwargs):
        dataset.headers.append('created_by')
        user_col = [kwargs['user'].id for row in dataset]
        dataset.append_col(user_col, header='created_by')
        return super().before_import(dataset, *args, **kwargs)


class BarcodeAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = BarcodeResource


class WidgetAdmin(admin.ModelAdmin):

    form = WidgetForm

    inlines = [
        TicketInline,
    ]


class TicketImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class BarcodeImageAdmin(admin.ModelAdmin):

    list_display = ('merchant', 'barcode')
    readonly_fields = ('image',)

    def barcode(self, instance):
        return instance.barcode.barcode


admin.site.register(Widget, WidgetAdmin)
admin.site.register(Barcode, BarcodeAdmin)
admin.site.register(TicketImage, TicketImageAdmin)
admin.site.register(BarcodeImage, BarcodeImageAdmin)
admin.site.register(Bidder)
