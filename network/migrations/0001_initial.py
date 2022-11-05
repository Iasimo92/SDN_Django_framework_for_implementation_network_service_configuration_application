# Generated by Django 2.1.2 on 2022-11-05 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('host', models.CharField(max_length=70)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(blank=True, max_length=100)),
                ('device_type', models.CharField(blank=True, choices=[('router', 'Router'), ('switch', 'Switch'), ('firewall', 'Firewall')], max_length=30)),
                ('platform', models.CharField(blank=True, choices=[('cisco_ios', 'Cisco IOS'), ('cisco_iosxe', 'Cisco IOS XE')], max_length=30)),
            ],
        ),
    ]
