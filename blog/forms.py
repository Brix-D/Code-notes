from django import forms
from django.forms import ModelForm, Textarea, TextInput, FileInput, PasswordInput, EmailInput, HiddenInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import User
from .models import Note, Comment


class NoteForm(ModelForm):
    """Форма на основе класса модели Note"""
    class Meta:
        model = Note
        fields = ["title", "article", "picture"]
        widgets = {
            "title": TextInput(attrs={'placeholder': 'Название:'}),
            "article": Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': 'Текст:'}),
            "picture": FileInput(attrs={'id': 'upload-file'}),
        }


class CommentForm(ModelForm):
    """Форма на основе класса модели Comment"""
    class Meta:
        model = Comment
        fields = ["text", "parent"]
        widgets = {
            # "author": TextInput(attrs={'placeholder': 'Ваше имя:'}),
            "text": Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': 'Текст:'}),
            "parent": HiddenInput()
        }
        labels = {
            "text": "Текст:",
        }


class RegisterUserForm(UserCreationForm):
    """Форма для регистрации пользователей"""
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Ваш логин:', "autocomplete": "off"}))
    email = forms.EmailField(widget=EmailInput(attrs={'placeholder': 'Ваш e-mail:', "autocomplete": "off"}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Ваш пароль:', "autocomplete": "off"}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Повторите пароль:', "autocomplete": "off"}))

    def __init__(self, *args, **kwargs):
        """
        Переопределение конструктора формы, чтобы убрать атрибут автофокус
        у поля ввода имени пользователя, который унаследован у родителя формы
        https://stackoverflow.com/questions/21515605/remove-autofocus-attribute-from-field-in-django
        """
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginUserForm(AuthenticationForm):
    """Форма для авторизации пользователей"""
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Ваш логин:', "autocomplete": "off"}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Ваш пароль:', "autocomplete": "off"}))
