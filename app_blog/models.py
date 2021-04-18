# using Python 3.8.5
from django.urls import reverse
from django.utils.safestring import mark_safe

from app_news.models import User
from django.db import models


class Blog(models.Model):
    """Блоги"""
    title = models.CharField(max_length=100)
    text = models.TextField(default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    create_date = models.DateTimeField(auto_created=True, auto_now=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'pk': self.pk})

    def get_edit_absolute_url(self):
        return reverse('blog_edit', kwargs={'pk': self.pk})

    def get_delete_absolute_url(self):
        return reverse('blog_delete', kwargs={'pk': self.pk})


class Picture(models.Model):
    """картинки для блогов"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='images/')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def image_tag(self):
        if self.file:
            return mark_safe(f'<img src="{self.file.url}" style="width:50px;height:50px;">')
        else:
            return 'No Image'

    image_tag.short_description = 'Изображение'
