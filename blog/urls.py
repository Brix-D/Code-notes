from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name="blog"),  # Главная страница
    path('note/create/', views.add_note, name="addNote"),  # Добавить статью
    path('note/delete/<int:id>', views.delete_note, name="deleteNote"),  # Удалить статью
    path('note/edit/<int:id>', views.edit_note, name="editNote"),  # Удалить статью
    path('note/view/<int:id>', views.view_note, name="viewNote"),  # Просмотр статьи с указанным номером
    path('note/download/<int:id>', views.download_picture, name="download_pic"),  # Загрузка картинки
    path('comments/create/<int:id>', views.add_comment, name="addComment"),  # Добавление комментария
    # path('searchone', views.search_one, name="searchone"),  # Пути для Ajax-запросов
    path('search/', views.search_multy, name="searchmulty"),  # Поиск статей в базе данных
    path('register/', views.register_user, name="register"),  # Регистрация пользователя
    path('login/', views.login_user, name="login"),  # Авторизация пользователя
    path('logout/', views.logout_user, name="logout"),  # Авторизация пользователя
    path('language/change/', views.set_user_language, name="change_language"),  # смена языка отображения сайта
    path('qr-code/create', views.create_qr_code, name="get_QR"),
]
