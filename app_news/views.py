# using Python 3.8.5
from datetime import datetime, timedelta

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.timezone import make_aware
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.models import User, Group

from app_blog.models import Blog
from app_news.company import ABOUT_COMPANY, CONTACTS_COMPANY
from app_news.models import News, Comment, Profile, NewsEditor, Tag
from app_news.forms import NewsForm, CommentForm, ProfileForm, RegisterForm, TagForm
from django.contrib import messages


class SuccessRegisterView(TemplateView):
    template_name = 'app_news/success_register.html'


class RegisterEdit(FormView):
    form_class = RegisterForm
    template_name = 'app_news/register.html'
    success_url = 'success_register.html'

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        login(self.request, new_user)
        group = Group.objects.get(name='Simple_Users')
        new_user.groups.add(group)
        return super().form_valid(form)


class NewsDeleteView(DeleteView):
    model = News
    success_url = '/news'
    template_name = 'app_news/news_delete.html'

    def get_queryset(self):
        queryset = News.objects.filter(slug=self.kwargs['slug'])
        return queryset


@method_decorator(login_required, name='dispatch')
class NewsEditView(UpdateView):
    form_class = NewsForm
    template_name = 'app_news/news_edit.html'
    success_url = '/news'

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        all_tags = Tag.objects.all()
        page_context['all_tags'] = all_tags
        current_news = self.get_object()
        current_tags = current_news.get_tags()
        page_context['current_tags'] = current_tags
        return page_context

    def get_queryset(self):
        queryset = News.objects.filter(slug=self.kwargs['slug'])
        return queryset


@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    form_class = CommentForm

    template_name = 'app_news/comment_create.html'
    success_url = '/news'
    model = Comment

    def get_initial(self):
        result = super().get_initial()
        slug = self.kwargs['slug']
        current_news = News.objects.get(slug=slug)
        news_id = current_news.id
        result['news'] = news_id
        return result


@method_decorator(login_required, name='dispatch')
class CommentEditView(UpdateView):
    form_class = CommentForm
    template_name = 'app_news/comment_edit.html'
    success_url = '/news'
    model = Comment


@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    template_name = 'app_news/comment_delete.html'
    success_url = '/news'
    model = Comment


class CommentDetailView(DetailView):
    model = Comment
    context_object_name = 'comment'
    template_name = 'app_news/comment_detail.html'


@method_decorator(login_required, name='dispatch')
class NewsCreateView(CreateView):
    """Добавление новости"""
    form_class = NewsForm
    template_name = 'app_news/news_create.html'
    success_url = '/news'

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        return page_context

    def get_initial(self):
        fields_init = super().get_initial()
        fields_init['author'] = self.request.user
        return fields_init


class AuthorView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'app_news/authors_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        page_content = super().get_context_data()
        page_content['ordered_fields'] = ['username', 'last_name', 'first_name', ]
        page_content['labels'] = ['Ник', 'Имя', 'Фамилия']
        page_content['order_by'] = AuthorView.ordering
        return page_content

    def post(self, request: HttpRequest):
        AuthorView.ordering = request.POST.get(key='order_by')
        return redirect('authors')


class AuthorDetailView(DetailView):
    model = User

    context_object_name = 'author'
    template_name = 'app_news/author_detail.html'
    success_url = '/authors'

    def post(self, request, *args, **kwargs):
        current_user: User = self.get_object()
        current_profile = Profile.objects.get(user=current_user.id)
        profile_form = ProfileForm(request.POST, request.FILES, instance=current_profile)
        if profile_form.is_valid():
            group = Group.objects.get(name='Verify_Users')
            if profile_form.cleaned_data['is_verify']:
                current_user.groups.add(group)
            else:
                current_user.groups.remove(group)
            profile_form.save()
        return redirect('authors')

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        current_user = self.get_object()
        current_profile = Profile.objects.get(user=current_user.id)
        profile_form = ProfileForm(instance=current_profile)
        page_context['profile_form'] = profile_form
        return page_context


class NewsDetailView(DetailView):
    """
    Прсмотр детальной информации о новости
    Здесь добавляются коментарии к новости
    """
    model = News
    context_object_name = 'news'
    template_name = 'app_news/news_detail.html'

    def post(self, request, *args, **kwargs):
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            form_comment.save()
        obj = self.get_object()

        return HttpResponseRedirect(obj.get_absolute_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        page_content = super().get_context_data()
        current_user = self.request.user
        current_news = self.get_object().id
        form_comment = CommentForm(initial={'author': current_user, 'news': current_news})
        page_content['comment_add'] = form_comment
        users_in_this_page = NewsEditor.objects.filter(news=current_news)
        page_content['edit_this'] = users_in_this_page

        return page_content


class SaveValuesMixin:
    store_values = []

    def clear_saved(self):
        self.store_values.clear()

    def add_save_value(self, value):
        self.store_values.append(value)

    def get_save_values(self):
        return self.store_values


class NewsView(SaveValuesMixin, ListView):
    """Просмотр перечня новостей"""
    template_name = 'app_news/news_list.html'
    model = News
    ordering = 'create_date'
    context_object_name = 'news_list'
    store_names = ['name', ]
    store_values = []

    def get_context_data(self, *, object_list=None, **kwargs):
        page_content = super().get_context_data()
        current_date_time = datetime.today()
        current_date = current_date_time.strftime('%Y-%m-%d')
        page_content['ordered_fields'] = ['title', 'create_date', 'author']
        page_content['labels'] = ['Заголовок', 'Дата создания', 'Автор']
        page_content['order_by'] = NewsView.ordering
        page_content['list_style'] = 'main-news-list'
        stores = self.get_save_values()
        if len(stores) == 0:
            self.add_save_value('Все')
            self.add_save_value(current_date)
            self.add_save_value('False')
        save_values = self.get_save_values()
        page_content['tag_filter'] = save_values[0]
        page_content['date_filter'] = save_values[1]
        page_content['enable_date_filter'] = save_values[2]
        return page_content

    def post(self, request: HttpRequest):
        NewsView.ordering = request.POST.get(key='order_by')
        self.clear_saved()
        self.add_save_value(request.POST.get(key='filter_tag'))
        self.add_save_value(request.POST.get(key='filter-date'))
        self.add_save_value(request.POST.get(key='date-enable'))

        return redirect('news')

    def get_queryset(self):
        query = super().get_queryset()
        user: User = self.request.user
        if not user.has_perm('app_news.can_activate_news'):
            query = query.filter(status='publish')
        store_value = self.get_save_values()

        if len(store_value) > 0 and store_value[0] != 'Все':
            tag = Tag.objects.get(name=store_value[0])
            query = query.filter(tags=tag)
        if len(store_value) > 1 and store_value[2] == 'True':
            date = store_value[1]
            date_begin = datetime.strptime(date, '%Y-%m-%d')
            date_delta = timedelta(days=1)
            date_end = date_begin + date_delta
            date_begin = make_aware(date_begin)
            date_end = make_aware(date_end)
            query = query.filter(create_date__range=(date_begin, date_end))
        if query.count() == 0:
            messages.error(self.request, 'Пустая выборка !!')

        return query


class Index(TemplateView):
    """Просмотр главной страници """
    template_name = 'app_news/index.html'

    def get_context_data(self):
        count_news = News.objects.all().count()
        count_comments = Comment.objects.all().count()
        count_users = User.objects.all().count()
        count_blogs = Blog.objects.all().count()
        page_content = {
            'count_news': count_news,
            'count_comments': count_comments,
            'count_users': count_users,
            'count_blogs': count_blogs,
        }
        return page_content


class About(TemplateView):
    """Страница О компании"""
    template_name = 'app_news/about.html'

    def get_context_data(self):
        return ABOUT_COMPANY


class Contacts(TemplateView):
    """Страница Контакты"""
    template_name = 'app_news/contacts.html'

    def get_context_data(self):
        return CONTACTS_COMPANY


class TagCreate(CreateView):
    form_class = TagForm
    template_name = 'app_news/tag_create.html'
    success_url = '/news/'

    def form_valid(self, form):
        ret = super().form_valid(form)
        print('in form valid', ret)
        return ret
