import os

from django import forms
from django.contrib import admin

from conf.settings import BASE_DIR, BASE_TICKET_TEMPLATE_PATH

from .models import Ticket


class TicketForm(forms.ModelForm):

    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open(os.path.join(BASE_DIR, BASE_TICKET_TEMPLATE_PATH), 'r') as f:
            initial_template = f.read()

        self.fields['template'].initial = initial_template

    class Meta:
        model = Ticket
        exclude = ['pdf', ]


class TicketAdmin(admin.ModelAdmin):

    fields = (
        'widget', 'name', 'description', 'box_office_price', 'template',
        'min_accepted_bid', 'max_bid_attempts', 'pdf_link',
    )
    readonly_fields = ('pdf_link', )

    form = TicketForm


admin.site.register(Ticket, TicketAdmin)
