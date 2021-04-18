# using Python 3.8.5
import django.forms as forms
from app_news.models import News, Comment, Profile
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные Пароли \t Не совпадают')
        return cd['password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("title", 'text', 'author', 'status', 'tags')
        widgets = {
            'author': forms.HiddenInput(),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'news-create-form-tags'})
        }


class CommentForm(forms.ModelForm):
    author = forms.TextInput()
    news = forms.TextInput()

    class Meta:
        model = Comment
        fields = ['text', 'author', 'news']
        widgets = {
            'author': forms.TextInput(attrs={"class": "hidden"}),
            'news': forms.TextInput(attrs={"class": "hidden"}),
            'text': forms.Textarea(attrs={"class": "comment-text-add", "cols": 50, "rows": 10}),
        }


class Login(forms.ModelForm):
    username = forms.CharField(max_length=150, )

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'user', 'middle_name', 'is_verify','avatar']
        widgets = {

            'middle_name': forms.TextInput(attrs={"placeholder": "Отчество"}),
            'user': forms.HiddenInput(),

        }
