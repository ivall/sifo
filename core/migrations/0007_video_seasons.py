# Generated by Django 3.0.7 on 2021-01-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_link_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='seasons',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
