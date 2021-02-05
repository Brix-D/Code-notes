from django.urls import path
from . import views

urlpatterns = [
    path('like/<int:note_id>', views.add_like, name="like"),
    path('check/<int:note_id>', views.check_liked, name="is_liked"),
]
