from django.db import models


class Widget(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )

    internal_name = models.CharField(
        verbose_name="Internal name",
        max_length=255,
    )

    enabled = models.BooleanField(
        verbose_name="Is widget enabled",
        default=False,
    )

    tickets = models.ForeignKey(
        "Ticket",
        verbose_name="Tickets",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Ticket(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )

    description = models.TextField(
        verbose_name="Description",
    )

    box_office_price = models.DecimalField(
        verbose_name="Box office price",
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self):
        return self.name
