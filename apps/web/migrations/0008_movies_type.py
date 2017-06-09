# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20170206_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='type',
            field=models.CharField(null=True, max_length=10),
        ),
    ]
