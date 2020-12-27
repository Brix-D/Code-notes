from django.contrib import admin
from .models import Note, Comment

# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    """Таблица Note в админке"""
    list_display = ['id', 'title', 'article', 'created', 'picture']  # Поля отображаемые в админке
    list_display_links = ['id', 'title']  # Поля ссылки в админке
    search_fields = ['title', 'article']  # Поиск по заголовку и статьи в админке


class CommentAdmin(admin.ModelAdmin):
    """Таблица Comments в админке"""
    list_display = ['id', 'author', 'text', 'created', 'art']
    list_display_links = ['id', 'author', 'text']
    list_filter = ['author']  # фильтр по автору коммента
    search_fields = ['author', 'text']


admin.site.register(Note, NoteAdmin)
admin.site.register(Comment, CommentAdmin)
