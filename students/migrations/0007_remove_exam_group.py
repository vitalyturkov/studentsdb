# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-11 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_exam_exam_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='group',
        ),
    ]
