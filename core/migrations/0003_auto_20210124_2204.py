# Generated by Django 3.0.7 on 2021-01-24 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210124_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
