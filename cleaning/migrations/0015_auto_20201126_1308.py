# Generated by Django 3.1.3 on 2020-11-26 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0014_auto_20201126_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cln_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Tidak Bersih', 'Tidak Bersih'), ('Bersih', 'Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='cln_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Tidak Bersih', 'Tidak Bersih'), ('Bersih', 'Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
