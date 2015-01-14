# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0011_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='activity',
            name='activityType',
            field=models.ForeignKey(to='volunteers.ActivityType'),
            preserve_default=True,
        ),
    ]
