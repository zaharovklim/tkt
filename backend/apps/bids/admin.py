from django.contrib import admin

from apps.bids.models import Bid, Order


class BidAdmin(admin.ModelAdmin):

    list_filter = ('ticket', 'status')

    list_display = (
        'ticket', 'session_key', 'bid_price', 'created_at', 'status',
    )


class OrderAdmin(admin.ModelAdmin):

    list_filter = ('bid__ticket', 'is_paid', )

    search_fields = ('bid__ticket__name', )

    list_display = (
        'bid', 'created_at', 'number_of_tickets', 'ip_address',
        'article_title', 'first_name', 'last_name', 'email', 'is_paid',
    )

admin.site.register(Bid, BidAdmin)
admin.site.register(Order, OrderAdmin)
