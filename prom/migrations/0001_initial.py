# Generated by Django 3.2.15 on 2022-10-13 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True)),
                ('display', models.CharField(max_length=50, unique=True)),
                ('fields_attr', models.JSONField()),
                ('rule_template', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expr', models.CharField(db_index=True, max_length=500, unique=True)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prom.metric')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_at', models.DateTimeField()),
                ('raw_content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prom.rule')),
            ],
        ),
    ]