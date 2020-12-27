from django.forms import ModelForm, Textarea, TextInput
from .models import Note, Comment


class NoteForm(ModelForm):
    """Форма на основе класса модели Note"""
    class Meta:
        model = Note
        fields = ["title", "article", "picture"]
        widgets = {
            "title": TextInput(),
            "article": Textarea(attrs={'cols': 30, 'rows': 10})
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

