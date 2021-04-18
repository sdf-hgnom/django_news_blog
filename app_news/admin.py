# using Python 3.8.5
from django.contrib import admin
from django.db.models import QuerySet
from app_news.models import News, Comment, Profile, NewsEditor,Tag


class CommentInline(admin.TabularInline):
    """Коментарии новости"""
    model = Comment
    list_display = ['text', 'author', 'create_date', ]
    fields = ['text', 'author', 'create_date']
    readonly_fields = ['create_date']
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    """для Комментариев"""
    list_display = ['trunc_text', 'author', 'create_date']
    fields = ['text', 'author', 'create_date', 'edit_date']
    readonly_fields = ['edit_date', 'create_date']
    sortable_by = ['author']
    actions = ['set_admin_delete']
    list_filter = ['author']

    def trunc_text(self, rec):
        """
        Для поля text принудительно установит длинну не более 15 символов
        Если больше обрежет и добавит '...'
        :param rec: текущая запись
        :return: скорректированный текст
        """
        if len(rec.text) > 15:
            result = rec.text[:12] + '...'
        else:
            result = rec.text
        return result

    trunc_text.short_description = 'Текст'

    def set_admin_delete(self, request, queryset: QuerySet):
        """
        установить текст - Удалено
        :param queryset: выборка пользователя
        :return: None
        """
        for rec in queryset:
            rec.text = 'Удалено Администратором'
            rec.save()
        self.message_user(request=request, message='Текст заменен на "Удалено Администратором"')

    set_admin_delete.short_description = 'Удалить сомнительный текст'


class NewsAdmin(admin.ModelAdmin):
    """Для Новостей"""
    list_display = ['title',
                    'author',
                    'create_date',
                    'edit_date',
                    'status',
                    'slug']
    list_filter = ['status']
    readonly_fields = ['slug']
    inlines = [CommentInline]
    sortable_by = 'status'
    actions = ('set_in_active', 'set_active')

    def set_active(self, request, queryset: QuerySet):
        """
        установить признак активности в true
        :param queryset: выборка пользователя
        :return: None
        """
        queryset.update(status='publish')

    def set_in_active(self, request, queryset: QuerySet):
        """
        установить признак активности в false
        :param queryset: выборка пользователя
        :return: None
        """
        queryset.update(active='draft')

    set_in_active.short_description = 'Перевести в статус Черновик'
    set_active.short_description = 'Перевести в статус Опубликованно'


class ProfileAdmin(admin.ModelAdmin):
    """Для профилей пользователя"""
    list_display = ['middle_name', 'phone', 'is_verify','city','image_tag']
    fields = ['middle_name', 'phone', 'is_verify','avatar','city','image_tag']
    readonly_fields = ['image_tag']


class NewsEditorAdmin(admin.ModelAdmin):
    """Для перечня редактирующих новость"""
    fields = ['news', 'user_key', 'date_begin']


class TagAdmin(admin.ModelAdmin):
    """Теги новостей"""
    fields = ['name']


admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(NewsEditor, NewsEditorAdmin)
admin.site.register(Tag,TagAdmin)
