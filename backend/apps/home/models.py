from django.db import models


class Widget(models.Model):

    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )

    internal_name = models.CharField(
        verbose_name="Internal name",
        max_length=255
    )

    enabled = models.BooleanField(
        verbose_name="Is widget enabled",
        default=False
    )
