# using Python 3.8.5
from django import template

from app_news.models import Tag

register = template.Library()


@register.filter(name='index')
def index(source, i: int):
    """
    Вернет значение по индексу
    :param source: итерируемый
    :param i: нужный индекс
    :return:
    """
    return source[i]


@register.inclusion_tag(filename='app_news/tags/comments_list.html')
def comment_list(what):
    context = {
        'comments': what,

    }
    return context


@register.inclusion_tag(filename='app_news/tags/order_by.html', name='order_by_form')
def order_by_form(fields, labels, order_by, filter_by=None, date_by=None, date_enable=None, style='order-by-line'):
    """
    Вставка формы для указания сортировок и фильтров по полям бд для модели News
    :param date_enable: включена-ли фильтрация по дате
    :param date_by:  дата для фильтрации
    :param filter_by: тэг фильтрации
    :param fields: поля сортировки
    :param labels: видимые названия полей (tag label)
    :param order_by: имя поля по которому отсортировано в данный момент (подставит checked)
    :param style : стиль для этой строки (по умолчанию класс order-by-line )
    :return:
    """
    tag_names = ['Все']
    all_tags = Tag.objects.all()
    for tag in all_tags:
        tag_names.append(tag.name)
    context = {
        'fields': fields,
        'labels': labels,
        'order_by': order_by,

        'style': style,

    }
    if filter_by is not None:
        filters = {
            'current_filter': filter_by,
            'current_date': date_by,
            'all_tags': tag_names,
            'filter_date_enable': date_enable,
        }
        context = {**context, **filters}
    return context
