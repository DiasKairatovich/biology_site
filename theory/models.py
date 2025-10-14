from django.db import models
from tests.models import Test  # связь с тестами
from ckeditor.fields import RichTextField  # для окна на подобии word
from django.utils.text import slugify

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
    slug = models.SlugField(unique=True, blank=True) # фильтрация по тексту в url для re_path
    content = RichTextField() # WYSIWYG-редактор
    order = models.PositiveIntegerField(default=0)  # для сортировки внутри раздела
    test = models.OneToOneField(Test, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def save(self, *args, **kwargs):
        if not self.slug:
            # slugify превращает "Тест по анатомии" → "test-po-anatomii"
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.section.title} — {self.title}"
