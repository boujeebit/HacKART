# Generated by Django 3.2.15 on 2023-02-21 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='initialized',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]