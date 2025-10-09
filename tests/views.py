from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Test, Question, Result
from .forms import TestForm, QuestionFormSet, save_test_with_questions
from django.core.paginator import Paginator

def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"


# --- Вкладка "Практика" (список тестов для всех пользователей) ---
@login_required
def test_list(request):
    tests = Test.objects.all().annotate(q_count=Count("questions")).order_by("id")

    paginator = Paginator(tests, 10)  # 10 тестов на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tests/test_list.html", {
        "page_obj": page_obj,
        "tests": page_obj.object_list,
    })


# --- Мои тесты (только учителя) ---
@login_required
@user_passes_test(is_teacher)
def manage_tests(request):
    tests = (
        Test.objects.filter(author=request.user)
        .annotate(q_count=Count("questions"))
    )
    return render(request, "tests/manage_tests.html", {"tests": tests})


# --- Создание теста (только учителя) ---
@login_required
@user_passes_test(is_teacher)
def create_test(request):
    if request.method == "POST":
        test_form = TestForm(request.POST, request.FILES)
        formset = QuestionFormSet(request.POST, request.FILES, prefix="questions")

        if test_form.is_valid() and formset.is_valid():
            save_test_with_questions(test_form, formset, request.user)
            messages.success(request, "Тест успешно создан!")
            return redirect("manage_tests")
    else:
        test_form = TestForm()
        formset = QuestionFormSet(prefix="questions")

    return render(request, "tests/create_test.html", {
        "test_form": test_form,
        "formset": formset,
    })

# --- Редактирование теста (только автор / учитель) ---
@login_required
@user_passes_test(is_teacher)
def edit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)

    if request.method == "POST":
        test_form = TestForm(request.POST, request.FILES, instance=test)
        formset = QuestionFormSet(request.POST, request.FILES, instance=test, prefix="questions")

        if test_form.is_valid() and formset.is_valid():
            save_test_with_questions(test_form, formset, request.user)
            messages.success(request, "Тест обновлён!")
            return redirect("manage_tests")
    else:
        test_form = TestForm(instance=test)
        formset = QuestionFormSet(instance=test, prefix="questions")

    return render(request, "tests/create_test.html", {
        "test_form": test_form,
        "formset": formset,
    })

# --- Удаление теста (только автор / учитель) ---
@login_required
@user_passes_test(is_teacher)
def delete_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)

    if request.method == "POST":
        test.delete()
        messages.success(request, f"Тест «{test.title}» удалён.")
        return redirect("manage_tests")

    # отдельная страница подтверждения
    return render(request, "tests/confirm_delete_test.html", {"test": test})


# --- Прохождение теста (доступно всем авторизованным) ---
@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()

    # Подготавливаем удобные структуры для шаблона
    prepared_questions = []
    for q in questions:
        if q.question_type == "MCQ":
            options = [(1, q.option1), (2, q.option2), (3, q.option3), (4, q.option4)]
            options = [(num, text) for num, text in options if text]  # убираем пустые
            prepared_questions.append({"obj": q, "options": options})

        elif q.question_type == "MCQ_IMG":
            images = [(1, q.image1), (2, q.image2), (3, q.image3), (4, q.image4)]
            images = [(num, img) for num, img in images if img]  # только загруженные
            prepared_questions.append({"obj": q, "images": images})

        elif q.question_type == "TF":
            prepared_questions.append({"obj": q, "tf": True})

    if request.method == "POST":
        score = 0
        total = len(prepared_questions)

        for q in prepared_questions:
            question = q["obj"]
            selected = request.POST.get(f"q{question.id}")

            if question.question_type in ["MCQ", "MCQ_IMG"]:
                if selected and int(selected) == question.correct_option:
                    score += 1
            elif question.question_type == "TF":
                if (selected == "true" and question.correct_bool) or \
                   (selected == "false" and not question.correct_bool):
                    score += 1

        passed = score >= total / 2  # сдача, если >= половины правильных

        Result.objects.create(
            user=request.user,
            test=test,
            score=score,
            total=total,
            passed=passed
        )

        messages.success(request, f"Вы набрали {score} из {total}.")
        return redirect("statistics")  # например, на страницу статистики

    if not questions.exists():
        messages.warning(request, "В этом тесте пока нет вопросов.")
        return redirect("test_list")

    return render(
        request,
        "tests/take_test.html",
        {"test": test, "questions": prepared_questions},
    )

# --- Статистика: разная для учителя и ученика ---
@login_required
def statistics(request):
    if is_teacher(request.user):
        # Результаты по тестам, созданным учителем
        tests_qs = Test.objects.filter(author=request.user)
        test_id = request.GET.get("test")
        results = Result.objects.filter(test__in=tests_qs).select_related("user", "test").order_by("-date_taken")
        if test_id:
            results = results.filter(test_id=test_id)

        # простая агрегированная сводка по выбранному тесту (если выбран)
        summary = None
        if test_id:
            agg = results.aggregate(avg=Avg("score"), total=Count("id"))
            summary = {
                "avg_score": round(agg["avg"] or 0, 2),
                "attempts": agg["total"] or 0
            }

        return render(request, "tests/statistics.html", {
            "mode": "teacher",
            "tests": tests_qs,
            "results": results,
            "summary": summary,
            "selected_test_id": int(test_id) if test_id else None
        })
    else:
        # Студент видит только свои результаты
        results = Result.objects.filter(user=request.user).select_related("test").order_by("-date_taken")
        return render(request, "tests/statistics.html", {
            "mode": "student",
            "results": results
        })

@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.filter(question_type="MCQ")
    if request.method != "POST":
        return redirect("take_test", test_id=test.id)

    score = 0
    total = questions.count()

    for q in questions:
        selected = request.POST.get(f"q_{q.id}")
        try:
            selected = int(selected) if selected is not None else None
        except ValueError:
            selected = None
        if selected and q.correct_option == selected:
            score += 1

    percent = (score / total) if total else 0
    passed = percent >= 0.6  # порог 60%

    attempt = Result.objects.filter(user=request.user, test=test).count() + 1
    Result.objects.create(
        user=request.user,
        test=test,
        score=score,
        total=total,
        passed=passed,
        attempt=attempt,
        group=""  # при желании передавай группу
    )

    return render(request, "tests/test_result.html", {
        "test": test,
        "score": score,
        "total": total,
        "passed": passed,
        "percent": round(percent * 100, 2),
        "attempt": attempt,
    })
