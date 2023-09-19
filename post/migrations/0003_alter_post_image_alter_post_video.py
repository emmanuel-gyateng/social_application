# Generated by Django 4.2.3 on 2023-08-21 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0002_post_creator_post_likes_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/%Y"),
        ),
        migrations.AlterField(
            model_name="post",
            name="video",
            field=models.FileField(blank=True, null=True, upload_to="videos/%Y"),
        ),
    ]
