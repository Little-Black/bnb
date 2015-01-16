# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('volunteers', '0015_auto_20150115_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='staff',
            field=models.ForeignKey(related_name='staff', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(related_name='user', default=b'', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
