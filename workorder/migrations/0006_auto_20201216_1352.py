# Generated by Django 3.1.3 on 2020-12-16 06:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workorder', '0005_auto_20201215_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wo_rincian',
            name='briksUser',
            field=models.ForeignKey(blank=True, default='', limit_choices_to={'groups__name': 'briks'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='briksUser', to=settings.AUTH_USER_MODEL, verbose_name='Petugas BRIKS'),
        ),
        migrations.AlterField(
            model_name='wo_rincian',
            name='ospUser',
            field=models.ForeignKey(blank=True, default='', limit_choices_to={'groups__name': 'maker'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ospUser', to=settings.AUTH_USER_MODEL, verbose_name='Petugas OSP'),
        ),
    ]
