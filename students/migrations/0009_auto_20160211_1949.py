# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_auto_20160211_1503'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': '\u0406\u0441\u043f\u0438\u0442', 'verbose_name_plural': '\u0406\u0441\u043f\u0438\u0442\u0438'},
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.IntegerField(max_length=256, verbose_name='\u0411\u0456\u043b\u0435\u0442'),
        ),
    ]
