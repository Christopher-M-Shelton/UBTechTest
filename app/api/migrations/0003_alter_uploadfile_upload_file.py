# Generated by Django 4.1.7 on 2023-03-06 06:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_uploadfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uploadfile",
            name="upload_file",
            field=models.FileField(upload_to="files"),
        ),
    ]
