# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming_dispatch', '0004_stream_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='key',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='server',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
