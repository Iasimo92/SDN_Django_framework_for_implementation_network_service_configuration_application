# Generated by Django 4.0.4 on 2022-12-05 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_alter_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='secret',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
