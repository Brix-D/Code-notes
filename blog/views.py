from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Note, Comment, User
from .forms import NoteForm, CommentForm, RegisterUserForm, LoginUserForm


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
    # note = Note.objects.get(pk=id)
    note = get_object_or_404(Note, pk=id)
    comms = Comment.objects.filter(art__id=id)
    # comms = get_list_or_404(Comment, art__id=id)
    form = CommentForm()
    return render(request, 'comments.html', {"note": note, "comms": comms, "form": form})


@login_required(login_url='login')
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


@login_required(login_url='login')
def edit_note(request, id):
    """Редактирование статьи"""
    note = get_object_or_404(Note, pk=id)
    if request.method == "POST":
        if request.POST.get("deleteimg"):
            note.picture = ""
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect("viewNote", id=id)
    else:
        form = NoteForm(instance=note)
        return render(request, 'newnote.html', {"form": form, "mode": "edit", "id": id})


@login_required(login_url='login')
def delete_note(request, id):
    """Удаление статьи"""
    note = get_object_or_404(Note, pk=id)
    note.delete()
    return redirect("blog")


@login_required(login_url='login')
def add_comment(request, id):
    """Добавление комментария"""
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.art_id = id
            entry.author_id = request.user.pk
            entry.save()
            return redirect("viewNote", id=id)
    return redirect("viewNote", id=id)


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
    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        # Если пользователь уже авторизован
        # то ему нельзя получить доступ к страницам логина и регистрации
        return redirect('blog')
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(redirect_to)
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {"form": form, "redirect_to": redirect_to})


def login_user(request):
    """
    Авторизация пользователя
    Редирект на предыдущую страницу осуществляется с помощью get параметра,
    который в свою очередь подставляется в шаблоне как request URI
    https://www.semicolonworld.com/question/53701/django-redirect-to-previous-page-after-login
    """

    redirect_to = request.GET.get('next')
    if request.user.is_authenticated:
        # Если пользователь уже авторизован
        # то ему нельзя получить доступ к страницам логина и регистрации
        return redirect('blog')
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(redirect_to)
    else:
        form = LoginUserForm()
    return render(request, 'login.html', {"form": form, "redirect_to": redirect_to})


@login_required(login_url='login')
def logout_user(request):
    """
    Выход текущего авторизованного пользователя из системы
    Если пользователь не авторизован то он не может выйти из аккаунта
    """
    redirect_to = request.GET.get('next')
    if redirect_to is None:
        # Для избежания циклических редиректов при logout/ -> login/?next=/logout -> logout/
        return redirect('blog')
    logout(request)
    return redirect(redirect_to)


def error404(request, exception):
    """Обработчик 404 страницы"""
    return render(request, '404.html')

