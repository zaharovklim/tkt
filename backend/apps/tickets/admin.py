import os

from django import forms
from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from conf.settings import BASE_DIR, BASE_TICKET_TEMPLATE_PATH, MEDIA_URL, CKEDITOR_JQUERY_URL

from import_export import resources
from import_export.admin import ExportMixin
from nested_admin import NestedStackedInline, NestedModelAdmin
from weekday_field.fields import WeekdayField

from .models import Article, Discount, DiscountSettings


class TicketForm(forms.ModelForm):

    name = forms.CharField()
    internal_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(os.path.join(BASE_DIR, BASE_TICKET_TEMPLATE_PATH), 'r') as f:
            initial_template = f.read()

        self.fields['template'].initial = initial_template

    class Meta:
        model = Article
        exclude = ('pdf', )


class TicketResource(resources.ModelResource):

    class Meta:
        model = Article
        exclude = ('template', 'pdf')


class DiscountSettingsInline(NestedStackedInline):
    model = DiscountSettings
    extra = 1
    fk_name = 'related_discount'

    formfield_overrides = {
        WeekdayField: {'widget': CheckboxSelectMultiple},
    }

    def clean(self):
        print(self.pk)


class DiscountInline(NestedStackedInline):
    model = Discount
    extra = 1
    fk_name = 'related_article'
    inlines = [DiscountSettingsInline]


class TicketAdmin(ExportMixin, NestedModelAdmin):
    change_form_template = '/app/templates/admin/tickets/article/add/change_form.html'
    resource_class = TicketResource

    fields = (
        'widget', 'name', 'internal_name', 'description',
        'template', 'pdf_link', 'created_by'
    )
    readonly_fields = ('pdf_link', )
    form = TicketForm
    inlines = [DiscountInline]


admin.site.register(Article, TicketAdmin)
