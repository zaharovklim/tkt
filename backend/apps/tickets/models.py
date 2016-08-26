from django.db import models


class Ticket(models.Model):

    name = models.TextField(
        verbose_name="Name",
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
