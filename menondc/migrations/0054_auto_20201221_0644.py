# Generated by Django 3.1.3 on 2020-12-20 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0053_auto_20201217_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mendc_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Ok', 'Ok'), ('Not Ok', 'Not Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='mendc_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Ok', 'Ok'), ('Not Ok', 'Not Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]