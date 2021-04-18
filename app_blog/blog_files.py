# using Python 3.8.5
import os
import csv
from django.conf import settings
from app_news.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from app_blog.models import Blog


def handle_uploaded_file(f: InMemoryUploadedFile):
    file_dir = os.path.join(settings.MEDIA_ROOT, 'images/')
    file_name = os.path.join(file_dir, f.name)
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def handle_csv_file(f: InMemoryUploadedFile, user: User):
    file_data = f.read()
    file_string = file_data.decode('utf-8').split('\n')
    csv_reader = csv.DictReader(file_string, delimiter=';', quotechar='"')
    for row in csv_reader:
        if settings.DEBUG:
            print(user)
            print(f"in csv file {row['b_name']} {row['b_text']} ")
        new_blog = Blog()
        new_blog.author = user
        new_blog.title = row['b_name']
        new_blog.text = row['b_text']
        new_blog.save()


def get_blog_download_file_list() -> list:
    """
    Вернет перечень файлов в дирректории сохранения файлов + /images
    Все загруженные файлы
    :return:
    """
    file_dir = os.path.join(settings.MEDIA_ROOT, 'images/')
    file_list = os.listdir(file_dir)
    file_list_path = ['images/' + item for item in file_list]

    return file_list_path
