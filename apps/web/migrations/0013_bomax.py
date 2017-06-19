# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20170610_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOMax',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('year', models.IntegerField()),
                ('collection', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'bo_max',
                'verbose_name': 'bo_max',
                'ordering': ('year',),
            },
        ),
    ]
