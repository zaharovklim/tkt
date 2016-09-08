from django.db import models

from apps.tickets.models import Ticket


class Bid(models.Model):

    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    PAID = 'PAID'
    BID_STATUSES = (
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (PAID, 'paid')
    )

    ticket = models.ForeignKey(
        Ticket,
        verbose_name="Ticket",
    )

    session_key = models.CharField(
        verbose_name="Session key",
        max_length=32
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
        return "{} - {} - {}".format(self.ticket, self.bid_price, self.status)


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

    number_of_tickets = models.SmallIntegerField(
        verbose_name="Number of tickets",
    )

    ip_address = models.GenericIPAddressField(
        verbose_name="IP Address",
        blank=True,
        null=True,
    )

    article_title = models.TextField(
        verbose_name="Article title",
        blank=True,
        null=True,
    )

    first_name = models.TextField(
        verbose_name="First name",
        blank=True,
        null=True,
    )

    last_name = models.TextField(
        verbose_name="Last name",
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name="E-mail",
    )

    is_paid = models.BooleanField(
        verbose_name="Is paid",
        default=False,
    )

    def __str__(self):
        return "{} ({}) - {} - {}".format(
            self.bid,
            self.number_of_tickets,
            self.created_at.replace(microsecond=0),
            'Paid' if self.is_paid else 'Waiting for payment'
        )
