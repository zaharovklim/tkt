from django.db import models
from django.contrib.auth.models import User


class ModelActionLogMixin(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        abstract = True
