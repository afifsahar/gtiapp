# Generated by Django 3.1.3 on 2021-01-04 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0068_auto_20210104_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cln_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Not Ok', 'Not Ok'), ('Ok', 'Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='cln_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Not Ok', 'Not Ok'), ('Ok', 'Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
