# using Python 3.8.5
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from app_news import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('about', views.About.as_view(), name='about'),
    path('contacts', views.Contacts.as_view(), name='contacts'),
    path('accounts/login', LoginView.as_view(template_name='app_news/login.html'), name='login'),
    path('accounts/logout', LogoutView.as_view(template_name='app_news/log_out.html'), name='logout'),
    path('accounts/register', views.RegisterEdit.as_view(success_url='success_register.html'), name='register'),
    re_path(r'success_register', views.SuccessRegisterView.as_view(), name='success_register'),
    path('accounts/profile/', views.AuthorView.as_view(), name='profile'),
    path('news/<str:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<str:slug>/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
    path('news/<str:slug>/<int:pk>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
    path('news/<str:slug>/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('news/<str:slug>/create_comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('news_edit/<str:slug>/', views.NewsEditView.as_view(), name='news_edit'),
    path('news_delete/<str:slug>/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('news_create', views.NewsCreateView.as_view(), name='news_create'),
    path('news', views.NewsView.as_view(), name='news'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/', views.AuthorView.as_view(), name='authors'),
]
