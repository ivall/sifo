# Generated by Django 3.0.7 on 2021-01-26 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_episode_episode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='title',
            field=models.CharField(max_length=128),
        ),
    ]