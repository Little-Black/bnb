# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0008_auto_20150112_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificationrequest',
            name='code',
            field=models.CharField(default=b'vlnmjlcftlxhHpmbhEJh', max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='verificationrequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
