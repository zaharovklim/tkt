from django.contrib import admin

from apps.bids.models import Bid, Order, Buyer


class BidAdmin(admin.ModelAdmin):

    list_filter = ('article', 'status')

    list_display = (
        'article', 'bid_price', 'created_at', 'status',
    )


admin.site.register(Bid, BidAdmin)
admin.site.register(Order)
admin.site.register(Buyer)
