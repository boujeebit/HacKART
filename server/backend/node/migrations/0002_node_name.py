# Generated by Django 3.2.15 on 2023-02-24 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
