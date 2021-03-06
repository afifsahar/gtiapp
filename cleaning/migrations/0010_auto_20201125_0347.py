# Generated by Django 3.1.3 on 2020-11-24 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0009_auto_20201125_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cln_daily',
            name='kondisi',
            field=models.CharField(blank=True, choices=[('Bersih', 'Bersih'), ('Tidak Bersih', 'Tidak Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
        migrations.AlterField(
            model_name='cln_default',
            name='defaultKondisi',
            field=models.CharField(blank=True, choices=[('Bersih', 'Bersih'), ('Tidak Bersih', 'Tidak Bersih')], default='', max_length=50, null=True, verbose_name='Kondisi'),
        ),
    ]
