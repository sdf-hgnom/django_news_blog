# Generated by Django 2.2.17 on 2020-12-07 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0003_remove_picture_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Avatar',
        ),
    ]
