# Generated by Django 4.2.5 on 2023-12-07 19:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0009_alter_review_nombre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comentarios",
            name="ranking",
            field=models.DecimalField(decimal_places=1, max_digits=1),
        ),
    ]