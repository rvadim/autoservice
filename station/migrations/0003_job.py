# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 12:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0002_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(verbose_name='Arrival time')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='station.Client')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='station.Service')),
                ('stand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='station.Stand')),
            ],
        ),
    ]
