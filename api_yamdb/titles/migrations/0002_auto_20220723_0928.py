# Generated by Django 2.2.16 on 2022-07-23 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("titles", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["id"]},
        ),
        migrations.AlterModelOptions(
            name="genre",
            options={"ordering": ["id"]},
        ),
        migrations.AlterModelOptions(
            name="title",
            options={"ordering": ["id"]},
        ),
    ]
