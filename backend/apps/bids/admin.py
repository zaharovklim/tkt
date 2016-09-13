from django.contrib import admin

from apps.bids.models import Bid, Order, Buyer


class BidAdmin(admin.ModelAdmin):

    list_filter = ('article', 'status')

    list_display = (
        'article', 'bid_price', 'created_at', 'status',
    )


# class OrderAdmin(admin.ModelAdmin):

#     list_filter = ('bid__article', 'is_paid', )

#     search_fields = ('bid__article__name', )

#     list_display = (
#         'bid', 'created_at', 'number_of_tickets', 'ip_address',
#         'article_title', 'first_name', 'last_name', 'email', 'is_paid',
#     )

admin.site.register(Bid, BidAdmin)
admin.site.register(Order)
admin.site.register(Buyer)
