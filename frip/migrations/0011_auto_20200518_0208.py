# Generated by Django 3.0.6 on 2020-05-18 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frip', '0010_auto_20200517_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frip',
            name='duedate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
