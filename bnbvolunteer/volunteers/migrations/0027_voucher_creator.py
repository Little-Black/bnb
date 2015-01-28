# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('volunteers', '0026_auto_20150127_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='creator',
            field=models.ForeignKey(default='defaultCreator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
