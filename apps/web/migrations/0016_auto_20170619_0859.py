# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_auto_20170617_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='movies',
            field=models.ManyToManyField(to='web.Movies'),
        ),
        migrations.AlterUniqueTogether(
            name='map_usermovie',
            unique_together=set([('uobj', 'mobj')]),
        ),
    ]
