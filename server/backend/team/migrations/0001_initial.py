# Generated by Django 3.2.15 on 2023-02-21 16:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=256, unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
        ),
    ]
