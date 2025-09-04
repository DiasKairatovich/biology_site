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
            "text": forms.Textarea(attrs={"rows": 1, "class": "form-control"}),
            "question_type": forms.Select(attrs={"class": "form-select"}),
            "correct_option": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 4}
            ),
            "correct_bool": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        q_type = cleaned_data.get("question_type")

        # Пропускаем валидацию для пустых форм
        if (not self.instance.pk and
                not any(cleaned_data.get(field) for field in ['text', 'option1', 'image1']) and
                not cleaned_data.get('DELETE')):
            return cleaned_data

        option_fields = ["option1", "option2", "option3", "option4"]
        image_fields = ["image1", "image2", "image3", "image4"]

        if q_type == "MCQ":
            # обнуляем ненужные
            cleaned_data["correct_bool"] = None
            for f in image_fields:
                cleaned_data[f] = None

            value = cleaned_data.get("correct_option")
            if value is None or value == "":
                raise forms.ValidationError("Для MCQ необходимо указать правильный вариант ответа.")

            try:
                int_value = int(value)
                if not (1 <= int_value <= 4):
                    raise forms.ValidationError("Правильный вариант должен быть числом от 1 до 4.")
            except (ValueError, TypeError):
                raise forms.ValidationError("Правильный вариант должен быть числом от 1 до 4.")

        elif q_type == "MCQ_IMG":
            # обнуляем текстовые варианты
            for f in option_fields:
                cleaned_data[f] = ""
            cleaned_data["correct_bool"] = None

            value = cleaned_data.get("correct_option")
            if value is None or value == "":
                raise forms.ValidationError("Для MCQ с картинками нужно указать правильный вариант.")

            try:
                int_value = int(value)
                if not (1 <= int_value <= 4):
                    raise forms.ValidationError("Правильный вариант должен быть числом от 1 до 4.")
            except (ValueError, TypeError):
                raise forms.ValidationError("Правильный вариант должен быть числом от 1 до 4.")

            if not any([cleaned_data.get(f) for f in image_fields]):
                raise forms.ValidationError("Добавьте хотя бы одну картинку.")

        elif q_type == "TF":
            # обнуляем варианты и картинки
            cleaned_data["correct_option"] = None
            for f in image_fields:
                cleaned_data[f] = None
            for f in option_fields:
                cleaned_data[f] = ""

            if cleaned_data.get("correct_bool") is None:
                raise forms.ValidationError("Для True/False нужно выбрать правильный ответ.")

        return cleaned_data


QuestionFormSet = inlineformset_factory(
    Test,
    Question,
    form=QuestionForm,
    extra=1,
    can_delete=True
)


def save_test_with_questions(test_form, formset, author):
    """Сохраняем тест и вопросы атомарно"""
    with transaction.atomic():
        test = test_form.save(commit=False)
        if not test.pk:
            test.author = author
        test.save()

        # Сохраняем формы formset
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                instance.test = test
            instance.save()

        # Удаляем отмеченные для удаления вопросы
        for obj in formset.deleted_objects:
            obj.delete()

        return test