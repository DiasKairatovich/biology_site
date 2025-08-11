from django.contrib import admin
from .models import Test, Question, Result

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test', 'question_type')
    list_filter = ('test', 'question_type')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'total', 'passed', 'date_taken')
    list_filter = ('test', 'passed', 'date_taken')
