# using Python 3.8.5
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, DetailView, CreateView, DeleteView
from typing import List

from app_blog.blog_files import handle_csv_file
from app_blog.forms import BlogsUploadForm, BlogEditForm
from app_blog.models import Blog, Picture


class BlogRightsRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        blog = Blog.objects.get(**kwargs)
        user_in_blog = blog.author
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not (request.user.is_superuser or request.user == user_in_blog):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class BlogDelete(BlogRightsRequiredMixin, DeleteView):
    raise_exception = True
    model = Blog
    success_url = reverse_lazy('blog_list')
    template_name = 'app_blog/blog_delete.html'


class BlogAdd(LoginRequiredMixin, CreateView):
    """Добавить блог """
    raise_exception = True
    form_class = BlogEditForm
    template_name = 'app_blog/blog_add.html'
    success_url = '/blog/blogs'

    def form_valid(self, form):
        if form.is_valid():
            new_blog: Blog = form.save(commit=False)
            new_blog.author = self.request.user
            new_blog.save()
        return super().form_valid(form)


class BlogEdit(BlogRightsRequiredMixin, TemplateView):
    """Редактировать блог"""
    template_name = 'app_blog/blog_edit.html'
    model = Blog
    raise_exception = True

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, **kwargs)
        is_change = False
        user_title = request.POST['title']
        user_text = request.POST['text']
        if blog.title != user_title:
            blog.title = user_title
            is_change = True
        if blog.text != user_text:
            blog.text = user_text
            is_change = True
        if is_change:
            blog.save()

        for item in blog.files.all():
            key = f'file_{item.id}'
            if key not in request.POST:
                Picture.objects.filter(id=item.id).delete()
        if 'upload' in request.FILES:
            for item in request.FILES.getlist('upload'):
                picture = Picture.objects.create(blog=blog, file=item)
                picture.save()

        return HttpResponseRedirect(redirect_to=blog.get_absolute_url())

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        page_context['blog'] = get_object_or_404(Blog, **kwargs)
        return page_context


class BlogDetail(DetailView):
    """Просмотр блога"""
    template_name = 'app_blog/blog_detail.html'
    model = Blog
    context_object_name = 'blog'


class BlogList(ListView):
    """Просмотр списка всех блогов"""
    template_name = 'blog_list.html'
    model = Blog
    context_object_name = 'context'
    ordering = '-create_date'


class BlogUpload(LoginRequiredMixin, FormView):
    """Загрузитиь блоги из файла"""
    raise_exception = True
    form_class = BlogsUploadForm
    template_name = 'app_blog/upload.html'
    success_url = '/blog'

    def post(self, request, *args, **kwargs):
        upload_form = BlogsUploadForm(request.POST, request.FILES)

        if upload_form.is_valid():
            all_files: List[InMemoryUploadedFile] = request.FILES.getlist('files')

            for file in all_files:
                handle_csv_file(file, request.user)
        return super().post(request, *args, **kwargs)


class BlogMain(TemplateView):
    """Головная страница блогов"""
    template_name = 'app_blog/index.html'

    def get_context_data(self, **kwargs):
        page_context = super().get_context_data(**kwargs)
        page_context['count_blogs'] = Blog.objects.count()
        return page_context
