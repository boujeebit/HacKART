# Generated by Django 3.2.15 on 2023-02-21 16:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=256, unique=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True, unique=True)),
                ('balloon', models.IntegerField(choices=[(1, 'Green'), (2, 'Yellow'), (3, 'Red')], unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solves', to='game.challenge')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solves', to='node.node')),
            ],
        ),
    ]
