# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-06 03:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'quizzes'},
        ),
        migrations.RenameField(
            model_name='quiz',
            old_name='uestions',
            new_name='questions',
        ),
    ]
