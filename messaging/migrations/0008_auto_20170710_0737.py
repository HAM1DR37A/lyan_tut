# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0007_auto_20170710_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(default='media/pic/None/no-img.jpg', upload_to='media/pic/'),
        ),
    ]
