# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-29 07:40
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20160826_0903'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='pdf',
            field=models.FileField(default='default_path', upload_to='/media/', verbose_name='PDF file'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=ckeditor.fields.RichTextField(verbose_name='Description'),
        ),
    ]
