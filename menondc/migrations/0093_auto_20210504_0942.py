# Generated by Django 3.1.3 on 2021-05-04 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0092_auto_20210112_1947'),
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
