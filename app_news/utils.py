# using Python 3.8.5
from django.contrib.auth.models import Group


def create_groups():
    """Для создания нужных групп """
    simple_group, created = Group.objects.get_or_create(name='Simple_Users')
    verify_group, created = Group.objects.get_or_create(name='Verify_Users')
    moderator_group, created = Group.objects.get_or_create(name='Moderators')


