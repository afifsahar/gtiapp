# Generated by Django 3.1.3 on 2020-12-23 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0055_auto_20201223_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cln_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Ok', 'Ok'), ('Not Ok', 'Not Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='cln_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Ok', 'Ok'), ('Not Ok', 'Not Ok')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
