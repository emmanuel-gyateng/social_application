# Generated by Django 4.2.3 on 2023-08-21 23:02

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("group", "0002_group_created_at"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="groupmember",
            unique_together={("user", "group")},
        ),
    ]
