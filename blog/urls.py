from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name="blog"),  # Главная страница
    path('note/create/', views.add_note, name="addNote"),  # Добавить статью
    path('note/delete/<int:id>', views.delete_note, name="deleteNote"),  # Удалить статью
    path('note/edit/<int:id>', views.edit_note, name="editNote"),  # Удалить статью
    path('comments/<int:id>', views.comments, name="comments"),  # Просмотр статьи с указанным номером
    path('comments/create/<int:id>', views.add_comment, name="addComment"),  # Добавление комментария
    # path('searchone', views.search_one, name="searchone"),  # Пути для Ajax-запросов
    path('search/', views.search_multy, name="searchmulty"),  # Поиск статей в базе данных
]
