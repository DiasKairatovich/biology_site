from django import forms
from django.forms import inlineformset_factory
from django.db import transaction
from .models import Test, Question


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["title", "description", "category"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"})
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "text",
            "question_type",
            "option1", "option2", "option3", "option4",
            "image1", "image2", "image3", "image4",
            "correct_option",
            "correct_bool"
        ]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 1}),
            "question_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        q_type = cleaned_data.get("question_type")

        if q_type == "MCQ":
            if not cleaned_data.get("correct_option"):
                raise forms.ValidationError("Для MCQ необходимо указать правильный вариант ответа.")
        elif q_type == "MCQ_IMG":
            if not cleaned_data.get("correct_option"):
                raise forms.ValidationError("Для MCQ с картинками нужно указать правильный вариант.")
            if not any([cleaned_data.get("image1"), cleaned_data.get("image2"),
                        cleaned_data.get("image3"), cleaned_data.get("image4")]):
                raise forms.ValidationError("Добавьте хотя бы одну картинку.")
        elif q_type == "TF":
            if cleaned_data.get("correct_bool") is None:
                raise forms.ValidationError("Для True/False нужно выбрать правильный ответ.")

        return cleaned_data


QuestionFormSet = inlineformset_factory(
    Test,
    Question,
    form=QuestionForm, # универсальная форма для MCQ/TF
    extra=1, # показывает 1 пустую форму сразу
    can_delete=True
)


def save_test_with_questions(test_form, formset, author):
    """Сохраняем тест и вопросы атомарно"""
    with transaction.atomic():
        test = test_form.save(commit=False)
        if not test.pk:
            test.author = author
        test.save()
        formset.instance = test
        formset.save()
        return test
