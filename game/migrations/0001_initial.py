# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-06 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('sources', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=16, max_digits=18)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=16, max_digits=18)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uestions', models.ManyToManyField(through='game.Answer', to='game.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_type', models.CharField(max_length=128)),
                ('avg_retail_price', models.DecimalField(decimal_places=16, max_digits=18)),
                ('retail_price_measurement', models.CharField(max_length=128)),
                ('prep_yield_factor', models.DecimalField(decimal_places=16, max_digits=18)),
                ('size_of_cup_equivalent', models.DecimalField(decimal_places=16, max_digits=18)),
                ('size_of_cup_eq_measurement', models.CharField(max_length=128)),
                ('avg_price_per_cup', models.DecimalField(decimal_places=16, max_digits=18)),
                ('addendum', models.TextField(blank=True, null=True)),
                ('consumable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='game.Consumable')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Variant'),
        ),
        migrations.AddField(
            model_name='guess',
            name='question',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='guess',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Guess'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Quiz'),
        ),
    ]
