from django.db import models
from tests.models import Test  # связь с тестами
from django_ckeditor_5.fields import CKEditor5Field  # для окна на подобии word

class Section(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


class Topic(models.Model):
    section = models.ForeignKey(Section, related_name="topics", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = CKEditor5Field() # WYSIWYG-редактор
    order = models.PositiveIntegerField(default=0)  # для сортировки внутри раздела
    test = models.OneToOneField(Test, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return f"{self.section.title} — {self.title}"
