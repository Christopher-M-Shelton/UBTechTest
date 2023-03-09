import logging
import csv
import os
import io

import requests
from structlog import wrap_logger
from django.core.exceptions import ValidationError
from http import HTTPStatus
from datetime import datetime
from api.models import Book, FileLink

logger = wrap_logger(logging.getLogger())


class BookCSVHandler:
    def __init__(self, file, username, s3url, trace_id):
        super().__init__()
        self.file = file
        self.username = username
        self.s3url = s3url
        self.trace_id = trace_id
        self.log = logger.new(
            trace_id=trace_id,
        )

    def retrieve(self):
        text_file = io.TextIOWrapper(self.file, encoding="utf-8")
        try:
            books = []
            for row in csv.DictReader(text_file):
                book = Book(
                    title=row["Book Title"],
                    author=row["Book Author"],
                    publisher=row["Publisher"],
                    uuid=row["uuid"],
                    datePublished=datetime.strptime(
                        row["Date Published"], "%d/%m/%Y"
                    ).date(),
                    csv_file=os.path.basename(self.file.name),
                    owner=self.username
                )
                books.append(book)

            Book.objects.bulk_create(books)
        except ValidationError as e:
            self.log.error(
                "File failed validation", trace_id=self.trace_id, error=e
            )
            return e, HTTPStatus.BAD_REQUEST
        except Exception as e:
            self.log.error(
                "Failed to extract from csv", trace_id=self.trace_id, error=e
            )
            return e, HTTPStatus.BAD_REQUEST

        resp = Book.objects.filter(csv_file=os.path.basename(self.file.name))

        self.ping(self.s3url)
        self.log.info("Request Processed", trace_id=self.trace_id)
        return resp, HTTPStatus.OK

    def ping(self, s3url):
        response = requests.post(
            url="https://postman-echo.com/post",
            json=s3url,
        )
        self.log.info("Pinged postman", response=response)


def owner_link(filename, original_filename, username):
    file_link = FileLink(
        filename=filename, original_filename=original_filename, owner=username
    )
    file_link.save()
