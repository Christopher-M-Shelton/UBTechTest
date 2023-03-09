from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=60)
    publisher = models.CharField(max_length=60)
    uuid = models.UUIDField()
    datePublished = models.DateField()
    csv_file = models.CharField(max_length=250)
    owner = models.CharField(max_length=120)

    @staticmethod
    def validate_uuid(value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValidationError(f"{value} is not a valid UUID")

    def clean(self):
        self.validate_uuid(str(self.uuid))


class FileLink(models.Model):
    filename = models.CharField(max_length=160)
    original_filename = models.CharField(max_length=120)
    owner = models.CharField(max_length=120)
