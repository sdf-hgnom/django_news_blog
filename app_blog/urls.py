# using Python 3.8.5
from django.urls import path
from app_blog import views

urlpatterns = [
    path('', views.BlogMain.as_view(), name='blog_main'),
    path('blogs/', views.BlogList.as_view(), name='blog_list'),
    path('blogs/add/', views.BlogAdd.as_view(), name='blog_add'),
    path('blogs/<int:pk>/', views.BlogDetail.as_view(), name='blog_detail'),
    path('blogs/edit/<int:pk>/', views.BlogEdit.as_view(), name='blog_edit'),
    path('blogs/delete/<int:pk>/', views.BlogDelete.as_view(), name='blog_delete'),
    path('blogs_upload/', views.BlogUpload.as_view(), name='blog_upload'),

]
