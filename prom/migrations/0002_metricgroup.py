# Generated by Django 3.2.15 on 2022-10-14 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
