# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_topposter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='box_office'
        ),
        migrations.AddField(
            model_name='movies',
            name='box_office',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
