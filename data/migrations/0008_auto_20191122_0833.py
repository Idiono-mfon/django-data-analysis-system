# Generated by Django 2.2.7 on 2019-11-22 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_auto_20191122_0714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.CharField(max_length=40),
        ),
    ]
