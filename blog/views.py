from django.core import serializers
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Note, Comment, User
from .forms import NoteForm, CommentForm, RegisterUserForm, LoginUserForm
from django.contrib import messages
import os.path
from django.utils import translation
import qrcode
import random
import string
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
        messages.error(request, "Страницы с таким номером не существует")
    except PageNotAnInteger:
        articles = articles_paginator.page(1)
        # messages.error(request, "Номер страницы должен быть целым числом")
    return render(request, 'blog.html', {"data": articles})


def view_note(request, id):
    """Вывод всех комментариев для указанной записи"""
    # note = Note.objects.get(pk=id)
    note = get_object_or_404(Note, pk=id)
    comms = Comment.objects.filter(art__id=id, parent__isnull=True)
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
            messages.success(request, "Заметка успешно добавлена")
            return redirect("blog")
        else:
            messages.error(request, "Форма заполнена некорректно")
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
            messages.success(request, "Заметка успешно изменена")
            return redirect("viewNote", id=id)
        else:
            messages.error(request, "Форма заполнена некорректно")
    else:
        form = NoteForm(instance=note)
    return render(request, 'newnote.html', {"form": form, "mode": "edit", "id": id})


@login_required(login_url='login')
def delete_note(request, id):
    """Удаление статьи"""
    note = get_object_or_404(Note, pk=id)
    note.delete()
    messages.success(request, "Заметка успешно удалена")
    return redirect("blog")


@login_required(login_url='login')
def download_picture(request, id):
    """Функция скачивания картинки статьи"""
    note = get_object_or_404(Note, pk=id)
    file_path = note.picture.name
    if os.path.exists(file_path):  # Если файл существует
        return FileResponse(open(file_path, 'rb'), as_attachment=True)  # Отдает файл бразуеру как загрузка
    else:
        messages.error(request, "Файл не найден")
        # Добавляет сообщение об ошибке,
        # которое будет показано 1 раз на следующей странице
        return redirect('viewNote', id)


@login_required(login_url='login')
def add_comment(request, id):
    """Добавление комментария"""
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_object = None
            try:
                parent_id = int(request.POST.get('parent'))  # если скрытый инпут не пустой
            except:
                parent_id = None
            if parent_id:
                parent_object = Comment.objects.get(pk=parent_id)  # получить объект родительского комментария
                if parent_object:  # если объект найден
                    reply_comment = form.save(commit=False)
                    reply_comment.parent = parent_object
            entry = form.save(commit=False)
            entry.art_id = id
            entry.author_id = request.user.pk
            entry.save()
            messages.success(request, "Комментарий успешно добавлен")
            return redirect("viewNote", id=id)
        else:
            messages.error(request, "Форма заполнена некорректно")
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
            messages.success(request, "Вы успешно зарегистрированы")
            return redirect(redirect_to)
        else:
            messages.error(request, "При регистрации произошла ошибка")
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
            messages.success(request, f'Добро пожаловать {user.username}!')
            return redirect(redirect_to)
        else:
            messages.error(request,
                           "При авторизации произошла ошибка. Проверьте правильность введенного логина и пароля")
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
    messages.success(request, "Вы вышли из аккаунта")
    return redirect(redirect_to)


def set_user_language(request):
    """
    Изменяет язык интерфейса пользователя,
    текущий язык отображения сохраняет в куку,
    редиректит обратно на предыдущую страницу
    """
    language = request.POST.get('language')
    redirect_to = request.GET.get('next')
    translation.activate(language)
    response = redirect(redirect_to)
    response.set_cookie('lang', language)
    return response


def create_qr_code(request):
    """Генерация QR-кода с URL текущей страницы"""
    page = request.GET.get("page")
    # image = qrcode.make(request.get_host() + page)
    qr_generator = qrcode.QRCode(
        version=5,
        box_size=10,
        border=3
    )  # объект через который создается qr-код
    qr_generator.add_data(request.get_host() + page)  # добавление данных для кодирования
    qr_generator.make(fit=True)
    # fit=True задает поведение, такое что бы все QR-коды были нужного размера,
    # даже если данные умещаются в меньшем объеме
    image = qr_generator.make_image(fill='black', back_color='white')  # создание изображения с цветами
    img_name = generate_random_string(15)
    img_path = f'media/qrs/{img_name}.png'
    # file = tempfile.NamedTemporaryFile(suffix='.png', dir='media/qrs', delete=False)  # Создание временного файла
    # Баг - на винде временный файл нельзя автоматически удалять - permission denied,
    # поэтому был использован обычный механизм работы с файлами
    image.save(img_path)  # сохранение изображения
    return FileResponse(open(img_path, 'rb'), as_attachment=True)  # Скачивание картинки с QR-кодом


def generate_random_string(length):
    """
    Создание рандомной строки из символов
    ASCII верхнего и нижнего регистра
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def error404(request, exception):
    """Обработчик 404 страницы"""
    return render(request, '404.html')
