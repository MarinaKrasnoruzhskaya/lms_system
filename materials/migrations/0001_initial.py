# Generated by Django 5.1 on 2024-09-03 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите название курса",
                        max_length=150,
                        unique=True,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью(картинку)",
                        null=True,
                        upload_to="course/pictures",
                        verbose_name="Превью(картинка)",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание курса",
                        null=True,
                        verbose_name="Описание курса",
                    ),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите название урока",
                        max_length=100,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание урока",
                        null=True,
                        verbose_name="Описание урока",
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью(картинку)",
                        null=True,
                        upload_to="lesson/pictures",
                        verbose_name="Превью(картинка)",
                    ),
                ),
                (
                    "link_to_video",
                    models.URLField(
                        blank=True,
                        help_text="Загрузите ссылку на видео",
                        null=True,
                        verbose_name="Ссылка на видео",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        blank=True,
                        help_text="Выберите курс",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="materials.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "урок",
                "verbose_name_plural": "уроки",
                "ordering": ("title",),
            },
        ),
    ]
