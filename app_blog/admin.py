# using Python 3.8.5
from django.contrib import admin
from app_blog.models import Blog, Picture


class PictureInLine(admin.TabularInline):
    model = Picture
    list_display = ['file', 'image_tag']
    readonly_fields = ['image_tag']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_date']
    inlines = [PictureInLine]


class PictureAdmin(admin.ModelAdmin):
    list_display = ['blog', 'file', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Picture, PictureAdmin)
admin.site.register(Blog, BlogAdmin)
