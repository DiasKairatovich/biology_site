from django import forms
from .models import Section, Topic
from django_ckeditor_5.widgets import CKEditor5Widget

class SectionForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditor5Widget(config_name="default"),
        required=False,
        label="Описание"
    )

    class Meta:
        model = Section
        fields = ["title", "description"]

class TopicForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name="default")
    )
    class Meta:
        model = Topic
        fields = ["title", "content", "order", "test"]