# Generated by Django 2.2.7 on 2019-11-21 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20191121_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='data_id',
            new_name='data',
        ),
    ]