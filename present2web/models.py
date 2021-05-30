import uuid
from djmoney.models.fields import MoneyField
from django.db import models


class Color(models.Model):
    name = models.TextField(unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"
        db_table = "colors"


class Category(models.Model):
    name = models.TextField(unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "categories"


class Present(models.Model):
    name = models.TextField(unique=True, verbose_name="Название")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="presents",
        verbose_name="Категория",
    )
    color = models.ForeignKey(
        Color,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="presents",
        verbose_name="Цвет",
    )
    price = MoneyField(max_digits=8, decimal_places=2, default_currency="RUB")
    url = models.TextField(verbose_name="Ссылка на подарок")
    image = models.TextField(
        null=True, blank=True, verbose_name="Ссылка на изображение"
    )
    change_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подарок"
        verbose_name_plural = "Подарки"
        ordering = ("-change_date",)
        get_latest_by = "change_date"
        db_table = "presents"


class Answer(models.Model):
    formulation = models.TextField(
        unique=True, verbose_name="Формулировка"
    )

    def __str__(self):
        return self.formulation

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        db_table = "answers"


class Question(models.Model):
    TYPES = (
        (0, "Краткий ответ"),
        (1, "Развернутый ответ"),
        (2, "Один из списка"),
        (3, "Несколько из списка"),
        (4, "Дата"),
    )
    formulation = models.TextField(
        unique=True, verbose_name="Формулировка"
    )
    priority = models.IntegerField(verbose_name="Приоритет")
    type_answer = models.IntegerField(
        choices=TYPES, default=2, verbose_name="Тип ответа"
    )
    is_requried = models.BooleanField(
        default=True,
        choices=(
            (True, "Да"),
            (False, "Нет"),
        ),
        verbose_name="Обязательный вопрос",
    )
    answers = models.ManyToManyField(Answer, blank=True, related_name="questions")

    def __str__(self):
        return self.formulation

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ("priority",)
        db_table = "questions"


class TempUrl(models.Model):
    questionnaire_uuid = models.UUIDField(
        default=uuid.uuid4, verbose_name="Уникальный id для анкеты"
    )
    presents_uuid = models.UUIDField(
        default=uuid.uuid4, verbose_name="Уникальный id для подарков"
    )
    rules = models.TextField(
        blank=True, null=True, verbose_name="Правило вывода"
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="temp_urls",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Временная ссылка"
        verbose_name_plural = "Временные ссылки"
