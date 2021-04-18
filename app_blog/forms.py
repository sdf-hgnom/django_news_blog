# using Python 3.8.5
import django.forms as forms

from app_blog.models import Blog


class BlogsUploadForm(forms.Form):
    files = forms.FileField(required=True,
                            label='Файлы для загрузки',
                            widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'text/csv'}),
                            )


class BlogEditForm(forms.ModelForm):
    title = forms.CharField(max_length=200,  label='Заголовок',
                            widget=forms.TextInput(attrs={'placeholder': 'Заголовок блога'}))
    text = forms.CharField(label='Текст',widget=forms.Textarea(attrs={'placeholder': 'Текст блога'}))
    files = forms.FileField(label='Файлы для загрузки',required=False,
                            widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Blog
        fields = ['text','title']
