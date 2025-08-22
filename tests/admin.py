from django.contrib import admin
from .models import Test, Question, Result

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author')
    list_filter = ('category', 'author')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'question_type')
    list_filter = ('test', 'question_type')
    search_fields = ('text',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'total', 'passed', 'date_taken')
    list_filter = ('passed', 'date_taken', 'test')
    search_fields = ('user__username', 'test__title')
