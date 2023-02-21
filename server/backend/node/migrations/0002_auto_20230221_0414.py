# Generated by Django 3.2.15 on 2023-02-21 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='node',
            name='mac',
        ),
        migrations.AddField(
            model_name='node',
            name='machineid',
            field=models.CharField(blank=True, max_length=128, null=True, unique=True),
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=17, null=True)),
                ('gateway', models.CharField(blank=True, max_length=17, null=True)),
                ('mac', models.CharField(max_length=17, unique=True)),
                ('dns', models.CharField(blank=True, max_length=17, null=True)),
                ('node', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='networking', to='node.node')),
            ],
        ),
    ]