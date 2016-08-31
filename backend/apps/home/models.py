from django.db import models
from django.contrib.auth.models import User

from import_export import resources
from image_cropping import ImageRatioField

from apps.utils.models import ModelActionLogMixin


class Widget(ModelActionLogMixin):

    name = models.TextField(
        verbose_name="Name",
    )

    internal_name = models.TextField(
        verbose_name="Internal name",
    )

    enabled = models.BooleanField(
        verbose_name="Is widget enabled",
        default=False,
    )

    def __str__(self):
        return self.name


class Barcode(models.Model):

    article = models.IntegerField(
        verbose_name="Article",
        null=True,
        blank=True
    )

    barcode = models.BigIntegerField(
        verbose_name="Barcode",
        null = True,
        blank = True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def str(self):
        return self.barcode


class BarcodeResource(resources.ModelResource):
    class Meta:
        model = Barcode


class TicketImage(models.Model):
    merchant = models.ForeignKey(User)
    image = models.ImageField(
        upload_to='images',
        null=True,
        blank=True
    )
    cropped_img = ImageRatioField('image', '360x360')

    def __str__(self):
        return str(self.merchant)
