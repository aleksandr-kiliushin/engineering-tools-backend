# Generated by Django 3.1.5 on 2021-02-01 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('valves', '0005_equipment_discount_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='control_signal',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='setting_range',
        ),
        migrations.RemoveField(
            model_name='equipment',
            name='voltage',
        ),
    ]
