from django.db import models
from django.conf import settings  # вместо прямого импорта User

class Test(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.CharField(max_length=100, blank=True, verbose_name="Категория/Раздел")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tests",
        verbose_name="Автор"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    QUESTION_TYPES = [
        ('MCQ', 'Выбор одного ответа'),
        ('TF', 'Верно / Неверно'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='MCQ', verbose_name="Тип вопроса")

    # Для MCQ
    option1 = models.CharField(max_length=255, blank=True, verbose_name="Вариант 1")
    option2 = models.CharField(max_length=255, blank=True, verbose_name="Вариант 2")
    option3 = models.CharField(max_length=255, blank=True, verbose_name="Вариант 3")
    option4 = models.CharField(max_length=255, blank=True, verbose_name="Вариант 4")
    correct_option = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="Номер правильного варианта")

    # Для TF
    correct_bool = models.BooleanField(blank=True, null=True, verbose_name="Правильный ответ (Да/Нет)")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Result(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField(verbose_name="Баллы")
    total = models.IntegerField(verbose_name="Всего вопросов")
    passed = models.BooleanField(default=False, verbose_name="Тест пройден?")
    attempt = models.PositiveIntegerField(default=1, verbose_name="Попытка")
    group = models.CharField(max_length=50, blank=True, verbose_name="Класс/Группа")
    date_taken = models.DateTimeField(auto_now_add=True, verbose_name="Дата прохождения")

    def __str__(self):
        return f"{self.user.username} — {self.test.title} ({self.score}/{self.total})"

    @property
    def percentage(self):
        return round((self.score / self.total) * 100, 2) if self.total else 0

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
