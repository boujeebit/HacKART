# Generated by Django 3.2.15 on 2023-04-05 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0002_network_ssid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='ssid',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
