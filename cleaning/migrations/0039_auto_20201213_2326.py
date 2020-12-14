# Generated by Django 3.1.3 on 2020-12-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0038_auto_20201213_2317'),
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
