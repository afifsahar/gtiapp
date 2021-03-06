# Generated by Django 3.1.3 on 2020-12-11 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0036_auto_20201210_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mendc_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Not Ok', 'Not Ok'), ('Ok', 'Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='mendc_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Not Ok', 'Not Ok'), ('Ok', 'Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
