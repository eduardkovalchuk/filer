# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-16 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('upload', models.FileField(upload_to='files')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файли',
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('hashtags', models.TextField()),
                ('parrent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='searcher.Folder')),
            ],
            options={
                'verbose_name': 'Папка',
                'verbose_name_plural': 'Папки',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='parrent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='searcher.Folder'),
        ),
    ]
