# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-29 10:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('psb', '0002_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='procedure',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='psb.Procedure'),
        ),
        migrations.AlterField(
            model_name='record',
            name='vacant_time',
            field=models.DateTimeField(verbose_name='datetime'),
        ),
    ]
