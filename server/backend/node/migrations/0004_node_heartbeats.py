# Generated by Django 3.2.15 on 2023-02-21 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0003_network_subnet'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='heartbeats',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]