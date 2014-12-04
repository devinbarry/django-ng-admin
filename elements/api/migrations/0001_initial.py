# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import api.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('answer', models.CharField(help_text='eg. Waar', max_length=255, blank=True)),
                ('type', models.CharField(choices=[('correct', 'Correct'), ('incorrect', 'Incorrect')], max_length=15, default='correct')),
                ('result_title', models.CharField(help_text='Shown to the user after they choose this answer', max_length=255, blank=True)),
                ('result_description', models.TextField(help_text='Shown to the user after they choose this answer', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=api.models._upload_to, blank=True)),
                ('color', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Disclaimer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(default='Type disclaimer here.', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fragment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='Short name to help identify the video', max_length=255, blank=True)),
                ('code', models.CharField(help_text='OBEN Fragment code', max_length=255, blank=True)),
                ('video_id', models.CharField(help_text='ODI video code', max_length=255, blank=True)),
                ('share_url', models.CharField(max_length=255, blank=True)),
                ('start_time', models.PositiveIntegerField(null=True, help_text='start time of fragment in seconds', blank=True)),
                ('end_time', models.PositiveIntegerField(null=True, help_text='end time of fragment in seconds', blank=True)),
                ('deleted', models.BooleanField(editable=False, default=False, verbose_name='Deleted')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(null=True, upload_to=api.models._upload_to, blank=True)),
                ('color', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('question', models.TextField(default='', blank=True)),
                ('description', models.TextField(help_text='This might be the lead in to the answer', default='', blank=True)),
                ('deleted', models.BooleanField(editable=False, default=False, verbose_name='Deleted')),
                ('fragment', models.ForeignKey(null=True, to='api.Fragment', on_delete=django.db.models.deletion.SET_NULL, blank=True)),
                ('image', models.ForeignKey(null=True, to='api.Image', on_delete=django.db.models.deletion.SET_NULL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fragment',
            name='thumbnail',
            field=models.ForeignKey(null=True, to='api.Image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(null=True, to='api.Question', related_name='answers', on_delete=django.db.models.deletion.SET_NULL, blank=True),
            preserve_default=True,
        ),
    ]
