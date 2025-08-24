from django import forms
from .models import Section, Topic
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class SectionForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(),
        required=False,
        label="Описание"
    )

    class Meta:
        model = Section
        fields = ["title", "description"]

class TopicForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Topic
        fields = ["title", "content", "order", "test"]