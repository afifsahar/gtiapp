# Generated by Django 3.1.3 on 2020-11-26 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menondc', '0010_auto_20201126_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mendc_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('NOT OKE', 'NOT OKE'), ('OKE', 'OKE')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='mendc_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Bersih', 'Bersih'), ('Tidak Bersih', 'Tidak Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]