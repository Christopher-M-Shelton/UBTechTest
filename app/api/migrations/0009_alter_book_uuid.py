# Generated by Django 4.1.7 on 2023-03-07 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_book_id_alter_book_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="uuid",
            field=models.UUIDField(),
        ),
    ]
