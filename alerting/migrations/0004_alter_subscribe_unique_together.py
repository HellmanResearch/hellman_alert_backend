# Generated by Django 3.2.15 on 2022-10-14 13:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('alerting', '0003_subscribe_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscribe',
            unique_together={('name', 'user')},
        ),
    ]