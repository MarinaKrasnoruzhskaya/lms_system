from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Класс для пользователя"""

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите email",
    )

    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        **NULLABLE,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Класс для модели Платежи"""

    PAY_METHODS = (
        ("card", "Карта"),
        ("cash", "Наличные"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты",
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        help_text="Выберите курс",
        **NULLABLE,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        help_text="Выберите урок",
        **NULLABLE,
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        help_text="Введите сумму оплаты",
    )
    payment_method = models.CharField(
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
        choices=PAY_METHODS,
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
    )
    payment_status = models.CharField(
        verbose_name="Статус оплаты",
        blank=True,
        null=True,
        default="Awaiting payment",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Платеж {self.pk} от {self.payment_date} на сумму {self.payment_amount}. Оплатил: {self.user} "
