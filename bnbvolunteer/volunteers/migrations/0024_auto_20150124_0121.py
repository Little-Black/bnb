# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0023_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='credit',
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
