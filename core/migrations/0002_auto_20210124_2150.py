# Generated by Django 3.0.7 on 2021-01-24 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.CharField(max_length=800),
        ),
    ]