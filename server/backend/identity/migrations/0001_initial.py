# Generated by Django 3.2.15 on 2023-03-28 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Broker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.CharField(max_length=256)),
                ('port', models.IntegerField(default=8443)),
            ],
        ),
        migrations.CreateModel(
            name='Integration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('PF', 'Platform'), ('HB', 'Heartbeat')], max_length=2)),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('hint', models.CharField(max_length=128, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integrations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
