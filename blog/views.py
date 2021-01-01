from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Note, Comment
from .forms import NoteForm, CommentForm, RegisterUserForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


def blog(request):
    """Вывод всех записей страницы блог"""
    articles = Note.objects.all()
    articles_paginator = Paginator(articles, 3)
    current_page = request.GET.get("page")
    try:
        articles = articles_paginator.page(current_page)
    except EmptyPage:
        articles = articles_paginator.page(1)
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
    return render(request, 'blog.html', {"data": articles})


def view_note(request, id):
    """Вывод всех комментариев для указанной записи"""
    # Comment.objects.create(author="Димас", text="Хуяк хуяк и в продакшн!", art_id=id)
    # note = Note.objects.get(pk=id)
    note = get_object_or_404(Note, pk=id)
    comms = Comment.objects.filter(art__id=id)
    # comms = get_list_or_404(Comment, art__id=id)
    form = CommentForm()
    return render(request, 'comments.html', {"note": note, "comms": comms, "form": form})


def add_note(request):
    """Добавление статьи"""
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("blog")
    else:
        form = NoteForm()
    return render(request, 'newnote.html', {"form": form, "mode": "add"})


def edit_note(request, id):
    """Редактирование статьи"""
    note = get_object_or_404(Note, pk=id)
    if request.method == "POST":
        if request.POST.get("deleteimg"):
            note.picture = ""
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect("comments", id=id)
    else:
        form = NoteForm(instance=note)
        return render(request, 'newnote.html', {"form": form, "mode": "edit", "id": id})


def delete_note(request, id):
    """Удаление статьи"""
    note = get_object_or_404(Note, pk=id)
    note.delete()
    return redirect("blog")


def add_comment(request, id):
    """Добавление комментария"""
    if request.method == "POST":
        form = CommentForm(request.POST)
        print(form)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.art_id = id
            entry.save()
            return redirect("comments", id=id)
    else:
        form = CommentForm()
    return render(request, "comments.html", {"form": form})


# def search_one(request):
#     """Поиск по одной фразе для AJAX-запроса"""
#     response = {}
#     if request.is_ajax():
#         word = request.POST["one"]
#         if not word:
#             return JsonResponse(response)
#         data = Note.objects.filter(Q(title__icontains=word) | Q(article__icontains=word))
#         serialize_data = serializers.serialize('json', data)
#         response = serialize_data
#         return JsonResponse(response, safe=False)
#
#     return JsonResponse(response)


def search_multy(request):
    """Поиск по нескольким ксловам для AJAX-запроса"""
    response = {}
    if request.is_ajax():
        words = request.POST["multy"]
        if not words:
            return JsonResponse(response)
        array_words = words.split()
        # result_base = Note.objects.all()
        # result = []
        result = Note.objects.all()
        for w in array_words:
            q_list = Q()
            q_list |= Q(title__icontains=w)
            q_list |= Q(article__icontains=w)
            # result += result_base.filter(q_list)
            result = result.filter(q_list)

        serialize_data = serializers.serialize('json', result)
        response = serialize_data
        return JsonResponse(response, safe=False)

    return JsonResponse(response)


def register_user(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {"form": form})


def login_user(request):
    """Авторизация пользователя"""
    return render(request, 'login.html')


def error404(request, exception):
    """Обработчик 404 страницы"""
    return render(request, '404.html')

