# Generated by Django 3.1.3 on 2020-11-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0015_auto_20201126_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mendc_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Bersih', 'Bersih'), ('Tidak Bersih', 'Tidak Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
