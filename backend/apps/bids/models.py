from django.db import models

from apps.tickets.models import Article


class Buyer(models.Model):

    email = models.EmailField(
        verbose_name="E-mail",
    )

    firstname = models.CharField(
        verbose_name="First name",
        max_length=255,
        null=True,
        blank=True,
    )

    lastname = models.CharField(
        verbose_name="Last name",
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.email


class Bid(models.Model):

    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    PAID = 'PAID'
    BID_STATUSES = (
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (PAID, 'paid')
    )

    buyer = models.ForeignKey(
        Buyer,
        verbose_name="Buyer",
        null=True,
        blank=True,
    )

    article = models.ForeignKey(
        Article,
        verbose_name="Article",
    )

    bid_price = models.DecimalField(
        verbose_name="Bid price",
        max_digits=6,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        blank=True
    )

    status = models.CharField(
        verbose_name="Status",
        max_length=8,
        choices=BID_STATUSES,
        default=REJECTED,
    )

    number_of_tickets = models.SmallIntegerField(
        verbose_name="Number of tickets",
    )

    def __str__(self):
        return "{} - {} - {}".format(self.article, self.bid_price, self.status)


class Order(models.Model):

    bid = models.ForeignKey(
        Bid,
        verbose_name="Bid",
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now_add=True,
        blank=True,
    )

    is_paid = models.BooleanField(
        verbose_name="Is paid",
        default=False,
    )

    def __str__(self):
        return "{} ({})".format(
            self.bid,
            'Paid' if self.is_paid else 'Waiting for payment'
        )
