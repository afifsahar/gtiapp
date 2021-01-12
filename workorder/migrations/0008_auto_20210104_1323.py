# Generated by Django 3.1.3 on 2021-01-04 06:23

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0007_auto_20201216_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wo_description',
            name='categoryService',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Mechanical', 'Mechanical'), ('Electrical', 'Electrical'), ('Air Conditioner', 'Air Conditioner'), ('Security', 'Security'), ('Cleaning', 'Cleaning'), ('Civil/Architectur', 'Civil/Architectur'), ('Electronics', 'Electronics'), ('Others', 'Others')], max_length=92, null=True, verbose_name='Category Service'),
        ),
    ]