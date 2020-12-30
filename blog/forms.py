from fileinput import FileInput

from django.forms import ModelForm, Textarea, TextInput, FileInput
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
        fields = ["author", "text"]
        widgets = {
            "author": TextInput(attrs={'placeholder': 'Ваше имя:'}),
            "text": Textarea(attrs={'cols': 30, 'rows': 10, 'placeholder': 'Текст:'})
        }
        labels = {
            "author": "Ваше имя:",
            "text": "Текст:"
        }

