# Generated by Django 2.2.17 on 2020-12-04 01:51

import app_news.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, help_text='Введите заголовок новости', max_length=100, verbose_name='Заголовок')),
                ('slug', models.SlugField(allow_unicode=True, default='', help_text='Введите текстовое представление новости', max_length=100, unique=True, verbose_name='Метка новости')),
                ('text', models.TextField(help_text='Введите текст новости', verbose_name='Текст новости')),
                ('create_date', models.DateTimeField(auto_now_add=True, help_text='Введите дату создания новости', verbose_name='Дата создания')),
                ('edit_date', models.DateTimeField(auto_now=True, help_text='Введите дату редактирования новости', verbose_name='Дата редактирования')),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('publish', 'Опубликованна')], default='draft', help_text='Установите статус новости', max_length=15, verbose_name='Статус новости')),
                ('author', models.ForeignKey(help_text='Выберите автора новости', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор новости')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['create_date'],
                'permissions': [('can_activate_news', 'Может одобрить новость')],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='город', help_text='Город', max_length=50, verbose_name='Город')),
                ('phone', models.CharField(blank=True, default='нету', help_text='Телефон', max_length=100, verbose_name='Телефон')),
                ('middle_name', models.CharField(blank=True, default='Отчество', help_text='Отчество', max_length=100, verbose_name='Отчество')),
                ('is_verify', models.BooleanField(blank=True, choices=[(True, 'Верифицирован'), (False, 'Не Верифицирован')], default=False, help_text='Является-ли автором новостей', verbose_name='Автор новостей')),                ('avatar', models.FileField(blank=True,  upload_to='avatars/', verbose_name='Аватар')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'permissions': [('can_set_verify', 'Может установить верификацию')],
            },
        ),
        migrations.CreateModel(
            name='NewsEditor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_key', models.CharField(max_length=150, verbose_name='Ключ пользователя')),
                ('date_begin', models.DateTimeField(auto_now_add=True, verbose_name='Дата начала редактирования')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_news.News', verbose_name='Редактируемая новость')),
            ],
            options={
                'verbose_name': 'Редактирует новость',
                'verbose_name_plural': 'Редактируют новость',
            },
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app_news.Tag', verbose_name='Тэги'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edit_date', models.DateTimeField(auto_created=True, auto_now=True, help_text='Дата измениения', verbose_name='Дата редактирования коментария')),
                ('create_date', models.DateTimeField(auto_created=True, auto_now_add=True, help_text='Дата создания коментария', verbose_name='Дата создания коментария')),
                ('text', models.TextField(help_text='Введите текст коментария', verbose_name='Текст коментария')),
                ('author', models.ForeignKey(help_text='Автор коментария', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор коментария')),
                ('news', models.ForeignKey(help_text='К какой новости коментарий', on_delete=django.db.models.deletion.CASCADE, to='app_news.News', verbose_name='Новость')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['create_date'],
            },
        ),
    ]
