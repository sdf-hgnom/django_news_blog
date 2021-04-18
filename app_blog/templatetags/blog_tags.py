from django import template

register = template.Library()


@register.filter(name='file_name')
def index(source: str):
    """
    Вернет имя файла из строки 'dir/file_name'
    :param source: строка вида 'dir/file_name'
    :return: строку после '/'
    """
    names = source.split('/')
    return names[1]


@register.filter(name='text_clip')
def text_clip(source: str, leght: int):
    """
    Вернет имя файла из строки 'dir/file_name'
    :param source: строка вида 'dir/file_name'
    :return: строку после '/'
    """
    result = source
    if len(source) > leght:
        result = source[:leght - 3] + '...'
    return result
