# Generated by Django 4.2.3 on 2023-08-21 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0003_alter_groupmember_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
