# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-12 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at_in_db', models.DateTimeField(auto_now_add=True, null=True, verbose_name='mtr.utils:created at')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='mtr.utils:created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='mtr.utils:updated at')),
                ('url', models.SlugField()),
                ('is_private', models.BooleanField(default=False, verbose_name='sites:is private')),
            ],
            options={
                'verbose_name_plural': 'sites:sites',
                'verbose_name': 'sites:site',
                'abstract': False,
                'ordering': ('-created_at',),
            },
        ),
    ]
