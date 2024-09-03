from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    """ Класс для модели Курс """
    title = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Название курса',
        help_text='Введите название курса',
    )
    picture = models.ImageField(
        upload_to='course/pictures',
        verbose_name='Превью(картинка)',
        help_text='Загрузите превью(картинку)',
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name='Описание курса',
        help_text='Введите описание курса',
        **NULLABLE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """ Класс для модели Урок """
    title = models.CharField(
        max_length=100,
        verbose_name='Название урока',
        help_text='Введите название урока',
    )
    description = models.TextField(
        verbose_name='Описание урока',
        help_text='Введите описание урока',
        **NULLABLE,
    )
    picture = models.ImageField(
        upload_to='lesson/pictures',
        verbose_name='Превью(картинка)',
        help_text='Загрузите превью(картинку)',
        **NULLABLE,
    )
    link_to_video = models.URLField(
        max_length=200,
        verbose_name='Ссылка на видео',
        help_text='Загрузите ссылку на видео',
        **NULLABLE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name='Курс',
        help_text='Выберите курс',
        **NULLABLE,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('title',)
