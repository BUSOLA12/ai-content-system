# Generated by Django 5.2 on 2025-04-24 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content_generator", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="generatedcontent",
            name="content_type",
            field=models.CharField(default="article", max_length=100),
        ),
        migrations.AlterField(
            model_name="generatedcontent",
            name="topic",
            field=models.CharField(default="technology", max_length=50),
        ),
    ]
