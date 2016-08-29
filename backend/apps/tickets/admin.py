import os

from django.contrib import admin

from conf.settings import BASE_DIR, BASE_TICKET_TEMPLATE_PATH

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, *args, **kwargs):

        with open(os.path.join(BASE_DIR, BASE_TICKET_TEMPLATE_PATH), 'r') as f:
            initial_template = f.read()

        form = super().get_form(request, *args, **kwargs)
        form.base_fields['template'].initial = initial_template
        return form


admin.site.register(Ticket, TicketAdmin)
