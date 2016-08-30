# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-25 14:19
from __future__ import unicode_literals

from django.db import migrations


def create_base_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    for group in ("Admin", "Merchant"):
        Group.objects.create(name=group)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_base_groups),
    ]
