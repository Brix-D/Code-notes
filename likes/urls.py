from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:note_id>', views.add_like, name="like"),  # Добавление лайка
    path('unlike/<int:note_id>', views.remove_like, name="unlike"),  # Удаление лайка
    path('check/<int:note_id>', views.check_liked, name="is_liked"),  # проверка на статус лайка
]
