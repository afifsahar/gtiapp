# Generated by Django 3.1.3 on 2020-11-24 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mendc_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Tidak Bersih', 'Tidak Bersih'), ('Bersih', 'Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='mendc_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Tidak Bersih', 'Tidak Bersih'), ('Bersih', 'Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
