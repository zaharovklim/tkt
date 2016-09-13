from django import forms

from apps.bids.models import Bid, Buyer


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = (
            'article', 'bid_price', 'number_of_tickets',
        )


class BuyerForm(forms.ModelForm):

    class Meta:
        model = Buyer
        fields = (
            'email', 'firstname', 'lastname',
        )
