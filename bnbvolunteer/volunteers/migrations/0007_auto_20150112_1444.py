# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('volunteers', '0006_auto_20150112_0206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dateDone', models.CharField(max_length=200)),
                ('dateEntered', models.CharField(max_length=200)),
                ('activityType', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('credits', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=200)),
                ('credits', models.PositiveSmallIntegerField(default=0)),
                ('redemptionActivity', models.ForeignKey(default=b'', to='volunteers.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userlog',
            name='user',
        ),
        migrations.DeleteModel(
            name='Userlog',
        ),
    ]
