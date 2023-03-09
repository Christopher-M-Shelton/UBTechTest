import os
import logging
import pytest
import uuid
from app.handlers.process_csv import BookCSVHandler

os.environ["PYTHONASYNCIODEBUG"] = "1"


@pytest.mark.asyncio
def test_upload_csv_200(caplog):
    with caplog.at_level(logging.INFO):
        trace_id = str(uuid.uuid4())
        username = 'a_username'
        s3url = 'a_url'
        expected_resp = '[{"Book Title": "book one", "Book Author": "author one", "Publisher": "publisher one", "uuid": "1234", "Date Published": "12/10/2022"}, {"Book Title": "book two", "Book Author": "author two", "Publisher": "publisher two", "uuid": "4321", "Date Published": "13/04/2021"}, {"Book Title": "book three", "Book Author": "author three", "Publisher": "publisher three", "uuid": "2312", "Date Published": "03/01/2020"}, {"Book Title": "book four", "Book Author": "author four", "Publisher": "publisher four", "uuid": "4221", "Date Published": "30/03/2019"}, {"Book Title": "book five", "Book Author": "author five", "Publisher": "publisher five", "uuid": "2312", "Date Published": "01/07/2018"}]'
        with open("tests/testdata/bookcsv.csv") as file:
            resp = BookCSVHandler(file, username, s3url, trace_id=trace_id).retrieve()

        assert resp == expected_resp
        assert "Pinged postman" in caplog.text
