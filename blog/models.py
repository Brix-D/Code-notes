from django.db import models
# from django.db.models import ObjectDoesNotExist
from django.db.models.signals import post_delete, pre_save
from django.shortcuts import reverse
from django.dispatch import receiver


# Create your models here.


class Note(models.Model):
    """Статья"""
    title = models.TextField(max_length=100, blank=False, verbose_name='Название статьи')
    article = models.TextField(max_length=3000, blank=False, verbose_name='Текст статьи')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')  # поле даты и времени с текущим временем при создании
    picture = models.ImageField(upload_to="media/Images/%Y-%m-%d", blank=True, verbose_name="Фото статьи")

    # поле хранит название картинки, и папку куда следует загружать картинку, %Y-%m-%d дата загрузки в названии папки

    def get_absolute_url(self):
        """Метод для получения url экземпляра модели через представление"""
        return reverse("viewNote", kwargs={"id": self.pk})

    class Meta:
        verbose_name = "Статья"  # Челочекочитаемое имя для админки
        verbose_name_plural = "Статьи"
        ordering = ["-created"]

    def __str__(self):
        return self.title

    # Еще один способ, запасной вариант
    # def save(self, *args, **kwargs):
    #     """Переобпределение метода сохранения модели
    #      для обработки мусорных изображений,
    #      оставшихся после обновления"""
    #     try:
    #         this = Note.objects.get(pk=self.id)
    #         if this.picture != self.picture:
    #             this.picture.delete(save=False)  # отмена автоматического вызова метода save, что вызовет рекурсию
    #     except ObjectDoesNotExist:
    #         print("запись не существует")
    #     super(Note, self).save(*args, **kwargs)


@receiver(post_delete, sender=Note)
def submission_delete(sender, instance, **kwargs):
    """
    Удаление файла стетьи, при удалении самой статьи
    https://matthiasomisore.com/uncategorized/django-delete-file-when-object-is-deleted/
    """
    instance.picture.delete(False)


@receiver(pre_save, sender=Note)
def delete_old_file_on_save(sender, instance, **kwargs):
    """
    Удаление старого фото при обновлении статьи
    https://stackoverflow.com/questions/2878490/how-to-delete-old-image-when-update-imagefield
    """
    if instance.pk:  # При добавлении первичный ключ будет None
        try:
            old_picture = Note.objects.get(pk=instance.pk).picture  # Получение старого объекта фото
        except Note.DoesNotExist:  # Если запись не существует
            return
        else:
            new_picture = instance.picture  # Получение новго фото из объекта сигнала save - формы
            if old_picture and old_picture != new_picture:
                # Если старое фото существует и не равно новому фото,
                # то удалить старое
                old_picture.delete(save=False)
                # Удаление старого фото, save=False отменяет вызов метода save для избежания рекурсии,
                # сигнал save уже вызван когда управление перешло к этому обработчику


class Comment(models.Model):
    """Комментарий к статье"""
    author = models.TextField(max_length=45, blank=False, verbose_name='Автор комментария')
    text = models.TextField(max_length=400, blank=False, verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    art = models.ForeignKey(Note, on_delete=models.CASCADE, verbose_name='Номер статьи')

    # Внешний ключ на Id статьи, при удалении статьи
    # комментарии удаляются каскадно

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created"]  # базовая сортировка по убыванию даты

    def __str__(self):
        return self.text[0:10]
