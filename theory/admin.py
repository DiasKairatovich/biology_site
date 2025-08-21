from django.contrib import admin
from .models import Section, Topic

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1  # сколько пустых строк для новых тем

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title",)
    inlines = [TopicInline]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "test")
    list_filter = ("section",)
    search_fields = ("title", "content")
    ordering = ("section", "order")
