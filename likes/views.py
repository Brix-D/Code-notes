from django.shortcuts import render, get_object_or_404
from .models import Like, ContentType
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from blog.models import Note
# Create your views here.

"""
Система лайков была взята отсюда:
https://apirobot.me/posts/how-to-implement-liking-in-django
"""


def add_like_to_object(obj, user):
    """Добавляет лайк пользовтаеля к объекту"""
    object_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(content_type=object_type, object_id=obj.id, user=user)
    return like


def remove_like_from_object(obj, user):
    """Удаляет лайк пользователя с объекта"""
    object_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=object_type, object_id=obj.id, user=user).delete()


def is_liked_object(obj, user):
    """Проверяет лайкнул ли пользователь объект"""
    object_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=object_type, object_id=obj.id, user=user)
    return likes.exists()


@login_required(login_url='login')
def add_like(request, note_id):
    """Представление для добавления лайка"""
    response = {}
    if request.is_ajax():
        object_note = get_object_or_404(Note, pk=note_id)
        current_user = request.user
        add_like_to_object(object_note, current_user)
        response["status"] = True
        return JsonResponse(response)
    else:
        response["status"] = False
        return JsonResponse(response)


def check_liked(request, note_id):
    """Проверяет лайкнул ли текущий авторизованный пользователь данную запись"""
    response = {"status": False}
    if request.is_ajax():
        if not request.user.is_authenticated:
            return JsonResponse(response)
        object_note = get_object_or_404(Note, pk=note_id)
        current_user = request.user
        response["status"] = is_liked_object(object_note, current_user)
    return JsonResponse(response)
