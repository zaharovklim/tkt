from django.db import models
from django.contrib.auth.models import User, Group

from import_export import resources
from image_cropping import ImageRatioField

from apps.utils.models import ModelActionLogMixin


# TODO: maybe move to another application
# TODO: poor logic
# TODO: rectrict access if group is wrong
def get_role(self):
    groups = self.groups.all()

    merchant = Group.objects.get(name='Merchant')
    admin = Group.objects.get(name='Admin')

    if merchant in groups:
        return 'Merchant'  # TODO: use constants
    elif admin in groups:
        return 'Admin'
    else:
        raise ValueError(
            'User has no appropriate group, there only "Merchant" and "Admin" '
            'groups supported by system'
        )

User.add_to_class('get_role', get_role)


class UserManager(models.Manager):

    def get_objects_list_by_role(self, user):
        role = user.get_role()

        if role == 'Admin':
            return self.get_queryset()
        elif role == 'Merchant':
            return (user, )

User.add_to_class('objects', UserManager())


def bid_statistics(self):
    tickets = self.widget_set.all()
    statistics = {
        'accepted': 0,
        'paid': 0,
        'rejected': 0,
    }
    for ticket in tickets:
        ticket_statistics = ticket.bid_statistics
        statistics['accepted'] += ticket_statistics['accepted']
        statistics['paid'] += ticket_statistics['paid']
        statistics['rejected'] += ticket_statistics['rejected']

    return statistics

User.add_to_class('bid_statistics', bid_statistics)


class WidgetManager(models.Manager):

    def get_objects_list_by_role(self, user):
        role = user.get_role()
        if role == 'Admin':  # TODO use constants
            return self.get_queryset()
        elif role == 'Merchant':
            return self.get_queryset().filter(created_by=user)


class Widget(ModelActionLogMixin):

    objects = WidgetManager()

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

    @property
    def bid_statistics(self):
        tickets = self.ticket_set.all()
        statistics = {
            'accepted': 0,
            'paid': 0,
            'rejected': 0,
        }
        for ticket in tickets:
            ticket_statistics = ticket.bid_statistics
            statistics['accepted'] += ticket_statistics['accepted']
            statistics['paid'] += ticket_statistics['paid']
            statistics['rejected'] += ticket_statistics['rejected']

        return statistics

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
        null=True,
        blank=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.barcode)


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
