# Generated by Django 4.2.5 on 2023-12-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("general", "0010_alter_comentarios_ranking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comentarios",
            name="ranking",
            field=models.DecimalField(decimal_places=1, max_digits=10),
        ),
    ]
