# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20170205_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upcoming_movies',
            fields=[
                ('baseclass_ptr', models.OneToOneField(serialize=False, auto_created=True, to='web.BaseClass', parent_link=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('rtscore', models.FloatField(default=0, null=True)),
                ('boscore', models.FloatField(default=0, null=True)),
                ('box_office', models.CharField(max_length=100, null=True)),
                ('totalscore', models.FloatField(default=0, null=True)),
            ],
            bases=('web.baseclass',),
        ),
    ]
