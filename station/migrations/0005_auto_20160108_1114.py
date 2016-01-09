# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0004_auto_20160107_1813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='box',
            options={'verbose_name': 'Бокс', 'verbose_name_plural': 'Боксы'},
        ),
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='job',
            options={'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'Услуга', 'verbose_name_plural': 'Услуги'},
        ),
        migrations.AlterModelOptions(
            name='stand',
            options={'verbose_name': 'Рабочее место', 'verbose_name_plural': 'Рабочие места'},
        ),
        migrations.AlterModelOptions(
            name='station',
            options={'verbose_name': 'Организация', 'verbose_name_plural': 'Организации'},
        ),
        migrations.RemoveField(
            model_name='job',
            name='service',
        ),
        migrations.AddField(
            model_name='job',
            name='services',
            field=models.ManyToManyField(to='station.Service'),
        ),
        migrations.AlterField(
            model_name='box',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=12, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='job',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Подтверждён'),
        ),
        migrations.AlterField(
            model_name='job',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='Завершена'),
        ),
        migrations.AlterField(
            model_name='job',
            name='date_time',
            field=models.DateTimeField(verbose_name='Время прибытия'),
        ),
        migrations.AlterField(
            model_name='service',
            name='max_cost',
            field=models.PositiveIntegerField(verbose_name='Макс. стоимость'),
        ),
        migrations.AlterField(
            model_name='service',
            name='max_duration',
            field=models.DurationField(verbose_name='Макс. продолжительность'),
        ),
        migrations.AlterField(
            model_name='service',
            name='min_cost',
            field=models.PositiveIntegerField(verbose_name='Мин. стоимость'),
        ),
        migrations.AlterField(
            model_name='service',
            name='min_duration',
            field=models.DurationField(verbose_name='Мин. продолжительность'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='stand',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='Название'),
        ),
    ]