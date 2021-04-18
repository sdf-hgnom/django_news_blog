# using Python 3.8.5
import time
from typing import Text

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from django.utils.text import slugify


def translit(source: Text) -> Text:
    """Транслитерация для slug"""
    source = source.lower()
    rus = list('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
    lat = list('abvgdeejziiklmnoprctufhtcssmyteyy')
    result = ''
    for ch in source:
        if ch in rus:
            index = rus.index(ch)
            lat_ch = lat[index]
        else:
            lat_ch = ch
        result += lat_ch
    return result


def get_news_slug(source: Text) -> Text:
    """Сделать slug из строки source"""
    lat_source = translit(source)
    new_news_slug = slugify(lat_source, allow_unicode=True) + '-' + str(int(time.time()))
    return new_news_slug


class Tag(models.Model):
    """Тэги новостей"""
    name = models.CharField(max_length=30, verbose_name='Название', db_index=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Профили Пользователей"""
    AUTHOR_CHOICE = [
        (True, 'Верифицирован'),
        (False, 'Не Верифицирован'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=50,
                            blank=False,
                            verbose_name='Город',
                            help_text='Город',
                            default='город'
                            )
    phone = models.CharField(max_length=100,
                             default='нету',
                             verbose_name='Телефон',
                             help_text='Телефон',
                             blank=True,
                             )

    middle_name = models.CharField(max_length=100,
                                   default='Отчество',
                                   verbose_name='Отчество',
                                   help_text='Отчество',
                                   blank=True
                                   )
    is_verify = models.BooleanField(default=False,
                                    verbose_name='Автор новостей',
                                    help_text='Является-ли автором новостей',
                                    choices=AUTHOR_CHOICE,
                                    blank=True,
                                    )
    avatar = models.FileField('Аватар',
                              max_length=100,
                              blank=True,
                              upload_to='avatars/',
                              )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        permissions = [('can_set_verify', 'Может установить верификацию')]

    def image_tag(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" style="width:50px;height:50px;">')
        else:
            return 'No Avatar'
    image_tag.short_description = 'Изображение'


    @property
    def full_name(self):
        return f'{self.user.last_name} {self.user.first_name} {self.middle_name}'

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.user.pk})

    def is_simple(self):
        return self.user.groups.filter(name='Simple_Users').exists()

    def is_moderator(self):
        return self.user.groups.filter(name='Moderators').exists()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class News(models.Model):
    """Новости"""
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('publish', 'Опубликованна')
    )
    title = models.CharField(max_length=100,
                             verbose_name='Заголовок',
                             db_index=True,
                             help_text='Введите заголовок новости',
                             )
    slug = models.SlugField(max_length=100,
                            verbose_name='Метка новости',
                            unique=True,
                            allow_unicode=True,
                            null=False,
                            default='',
                            help_text='Введите текстовое представление новости',
                            )
    text = models.TextField(verbose_name='Текст новости', help_text='Введите текст новости')
    author = models.ForeignKey(User,
                               verbose_name='Автор новости',
                               on_delete=models.CASCADE,
                               help_text='Выберите автора новости',
                               )
    create_date = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания',
                                       help_text='Введите дату создания новости',
                                       )
    edit_date = models.DateTimeField(auto_now=True,
                                     verbose_name='Дата редактирования',
                                     help_text='Введите дату редактирования новости',
                                     )
    status = models.CharField(max_length=15,
                              choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статус новости',
                              help_text='Установите статус новости',
                              )
    tags = models.ManyToManyField(Tag, verbose_name='Тэги', blank=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['create_date']
        permissions = [
            ('can_activate_news', 'Может одобрить новость')
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def get_comment_create_absolute_url(self):
        return reverse('comment_create', kwargs={'slug': self.slug})

    def get_edit_absolute_url(self):
        return reverse('news_edit', kwargs={'slug': self.slug})

    def get_delete_absolute_url(self):
        return reverse('news_delete', kwargs={'slug': self.slug})

    def get_tags(self):
        tags = []
        for tag in self.tags.all():
            tags.append(tag.name)
        return ','.join(tags)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            self.slug = get_news_slug(self.title)
        super().save(force_insert, force_update, using, update_fields)


class Comment(models.Model):
    """Коментарии к новостям"""
    text = models.TextField(verbose_name='Текст коментария',
                            help_text='Введите текст коментария',
                            )
    news = models.ForeignKey(News,
                             verbose_name='Новость',
                             db_index=True,
                             on_delete=models.CASCADE,
                             help_text='К какой новости коментарий',
                             )
    author = models.ForeignKey(User,
                               db_index=True,
                               verbose_name='Автор коментария',
                               on_delete=models.CASCADE,
                               help_text='Автор коментария',
                               )
    create_date = models.DateTimeField(auto_created=True,
                                       auto_now_add=True,
                                       verbose_name='Дата создания коментария',
                                       help_text='Дата создания коментария',
                                       )
    edit_date = models.DateTimeField(auto_created=True,
                                     auto_now=True,
                                     verbose_name='Дата редактирования коментария',
                                     help_text='Дата измениения',
                                     )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['create_date']

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'slug': self.news.slug, 'pk': self.pk})

    def get_edit_absolute_url(self):
        return reverse('comment_edit', kwargs={'slug': self.news.slug, 'pk': self.pk})

    def get_delete_absolute_url(self):
        return reverse('comment_delete', kwargs={'slug': self.news.slug, 'pk': self.pk})



class NewsEditor(models.Model):
    """редактируют новость """
    news = models.ForeignKey(News, verbose_name='Редактируемая новость', on_delete=models.CASCADE)
    user_key = models.CharField(max_length=150, verbose_name='Ключ пользователя')
    date_begin = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала редактирования')

    class Meta:
        verbose_name = 'Редактирует новость'
        verbose_name_plural = 'Редактируют новость'
