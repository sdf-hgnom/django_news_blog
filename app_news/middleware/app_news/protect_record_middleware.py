
from django.contrib.auth import get_user
from django.urls import resolve
from app_news.models import News,NewsEditor
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import AnonymousUser


class ProtectNewsDetailPagesMiddleware:
    TIME_EXPIRE = timezone.timedelta(minutes=5)

    def __init__(self, get_response):
        self.get_response = get_response
        self.in_news_view_page = {}
        self.in_comment_edit_page = {}

    def __call__(self, request):
        ip_addr = request.META['REMOTE_ADDR']
        user = get_user(request)
        path = resolve(request.path).url_name
        current_time = timezone.now()
        session_id = request.session.session_key

        user_key = f'{ip_addr} @ {user} @ {session_id}'

        if path == 'news_detail':
            kwargs = resolve(request.path).kwargs
            news_slug = kwargs.get('slug')
            news_in_request = News.objects.get(slug=news_slug)
            editors_for_news = NewsEditor.objects.filter(news=news_in_request)
            expaire_date = current_time - ProtectNewsDetailPagesMiddleware.TIME_EXPIRE
            editors_for_news.filter(date_begin__lt=expaire_date).delete()
            editors_for_news.filter(user_key=user_key).delete()
            news_editor = NewsEditor(user_key=user_key, news=news_in_request)
            news_editor.save()
        response = self.get_response(request)


        return response

    def update_news_editors(self, news_slug, user_key):
        pass
