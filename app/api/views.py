from http import HTTPStatus
import uuid
import os
from itertools import groupby
from operator import attrgetter
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

from app.handlers.process_csv import BookCSVHandler, owner_link
from .models import Book
from .forms import UploadForm
from app.settings import MEDIA_ROOT


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "api/register.html", {"form": form})


@login_required(login_url="/account/login")
def upload_file(request):
    if request.method == "POST":
        username = request.user.username
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            original_name = uploaded_file.name
            uploaded_file.name = new_name = (
                os.path.splitext(original_name)[0]
                + "-"
                + str(uuid.uuid4())
                + os.path.splitext(original_name)[1]
            )

            path = default_storage.save(f"{MEDIA_ROOT}/{new_name}", uploaded_file)
            s3url = default_storage.url(path)

            owner_link(new_name, original_name, username)

            with default_storage.open(os.path.join(f"{MEDIA_ROOT}/{new_name}")) as file:
                resp, status = BookCSVHandler(
                    file, username, s3url, trace_id=str(uuid.uuid4())
                ).retrieve()

            data = {}
            if status != HTTPStatus.OK:
                data["error"] = resp
            else:
                data["book_list"] = resp
            data["form"] = UploadForm()
            return render(request, "api/uploadfile_form.html", data)
    else:
        form = UploadForm()
    return render(request, "api/uploadfile_form.html", {"form": form})


@login_required(login_url="/account/login")
def profile(request):
    username = request.user.username
    books = Book.objects.filter(owner=username).order_by("csv_file")

    books_by_csv_file = {}
    for csv_file, books_group in groupby(books, key=attrgetter("csv_file")):
        books_by_csv_file[csv_file] = list(books_group)
    return render(
        request,
        "api/profile.html",
        {
            "books_by_csv_file": books_by_csv_file,
        },
    )
