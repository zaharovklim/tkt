# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-26 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
        ('home', '0004_auto_20160826_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='widget',
            name='tickets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.Ticket', verbose_name='Tickets'),
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
