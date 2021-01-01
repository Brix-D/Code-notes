from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name="blog"),  # Главная страница
    path('note/create/', views.add_note, name="addNote"),  # Добавить статью
    path('note/delete/<int:id>', views.delete_note, name="deleteNote"),  # Удалить статью
    path('note/edit/<int:id>', views.edit_note, name="editNote"),  # Удалить статью
    path('note/view/<int:id>', views.view_note, name="viewNote"),  # Просмотр статьи с указанным номером
    path('comments/create/<int:id>', views.add_comment, name="addComment"),  # Добавление комментария
    # path('searchone', views.search_one, name="searchone"),  # Пути для Ajax-запросов
    path('search/', views.search_multy, name="searchmulty"),  # Поиск статей в базе данных
    path('register/', views.register_user, name="register"),  # Регистрация пользователя
    path('login/', views.login_user, name="login"),  # Авторизация пользователя
]
