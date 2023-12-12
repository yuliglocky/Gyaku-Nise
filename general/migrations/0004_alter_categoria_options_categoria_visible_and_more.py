# Generated by Django 4.2.4 on 2023-10-18 06:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0003_rename_rating_review_alter_categoria_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="categoria",
            options={},
        ),
        migrations.AddField(
            model_name="categoria",
            name="visible",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="comentarios",
            name="visible",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="producto",
            name="visible",
            field=models.BooleanField(default=True),
        ),
    ]
