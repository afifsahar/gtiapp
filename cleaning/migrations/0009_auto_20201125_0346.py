# Generated by Django 3.1.3 on 2020-11-24 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0008_auto_20201125_0318'),
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