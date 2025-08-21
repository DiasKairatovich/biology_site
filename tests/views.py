from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Test, Question, Result
from .forms import TestForm, QuestionFormSet, save_test_with_questions

# проверка на роль "учитель"
def is_teacher(user):
    return user.is_authenticated and getattr(user, "role", "") == "teacher"


# --- Вкладка "Практика" (список тестов для всех пользователей) ---
@login_required
def test_list(request):
    tests = Test.objects.all().annotate(q_count=Count("questions"))
    return render(request, "tests/test_list.html", {"tests": tests})


# --- Мои тесты (только учителя) ---
@login_required
def manage_tests(request):
    tests = (
        Test.objects.filter(author=request.user)
        .annotate(q_count=Count("questions"))
    )
    return render(request, "tests/manage_tests.html", {"tests": tests})


# --- Создание теста (только учителя) ---
@login_required
def create_test(request):
    if not request.user.groups.filter(name="Учителя").exists():
        messages.error(request, "Только учителя могут создавать тесты.")
        return redirect("test_list")

    if request.method == "POST":
        test_form = TestForm(request.POST)
        formset = QuestionFormSet(request.POST, prefix="questions")

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

@login_required
def edit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)

    if request.method == "POST":
        test_form = TestForm(request.POST, instance=test)
        formset = QuestionFormSet(request.POST, instance=test, prefix="questions")

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


@login_required
def delete_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id, author=request.user)

    if request.method == "POST":
        test.delete()
        messages.success(request, f"Тест «{test.title}» удалён.")
        return redirect("manage_tests")

    # отдельная страница подтверждения
    return render(request, "tests/confirm_delete.html", {"test": test})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    # Только MCQ вопросы
    questions = test.questions.filter(question_type="MCQ")

    for q in questions:
        q.options = [
            (1, q.option1),
            (2, q.option2),
            (3, q.option3),
            (4, q.option4),
        ]
        q.options = [(num, text) for num, text in q.options if text]

    if request.method == "POST":
        score = 0
        total = questions.count()

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected and int(selected) == q.correct_option:
                score += 1

        passed = score >= total / 2  # например, порог «сдал» = половина

        # Сохраняем результат
        Result.objects.create(
            user=request.user,
            test=test,
            score=score,
            total=total,
            passed=passed
        )

        messages.success(request, f"Вы набрали {score} из {total}.")
        return redirect("statistics")  # например, сразу на страницу статистики

    if not questions.exists():
        messages.warning(request, "В этом тесте пока нет вопросов.")
        return redirect("test_list")

    return render(request, "tests/take_test.html", {"test": test, "questions": questions})


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

@login_required
def statistics(request):
    if request.user.groups.filter(name="Учителя").exists():
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
