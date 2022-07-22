# Generated by Django 4.0.6 on 2022-07-22 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("titles", "0005_remove_title_genre_title_genre_genretitle"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="title",
            name="genre",
        ),
        migrations.AddField(
            model_name="title",
            name="genre",
            field=models.ManyToManyField(
                through="titles.GenreTitle", to="titles.genre"
            ),
        ),
    ]
