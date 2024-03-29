# Generated by Django 3.2.15 on 2023-03-28 16:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=256, unique=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('integration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='identity.integration')),
            ],
        ),
    ]
