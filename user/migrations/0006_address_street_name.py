# Generated by Django 3.1.7 on 2021-03-18 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210318_0923'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='street_name',
            field=models.CharField(default='CharField', max_length=100),
            preserve_default=False,
        ),
    ]
