# Generated by Django 3.1.3 on 2021-01-12 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0085_auto_20210112_0715'),
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
