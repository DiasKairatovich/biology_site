from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Test, Result
from .forms import TestForm, QuestionFormSet, save_test_with_questions
from django.core.paginator import Paginator
from django.utils import timezone
from django.conf import settings
from openpyxl import Workbook
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from .mixins import TeacherRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

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


# --- CBV Статистика: разная для учителя и ученика ---
class StatisticsView(LoginRequiredMixin, View):
    """Просмотр статистики: общая логика для учителя и студента."""

    def get(self, request):
        user = request.user

        if hasattr(user, "role") and user.role == "teacher":
            # --- Для учителя ---
            tests_qs = Test.objects.filter(author=user)
            test_id = request.GET.get("test")

            # Учитываем случай с 'None'
            if not test_id or test_id == "None":
                selected_test_id = None
                results = Result.objects.filter(test__in=tests_qs)
            else:
                selected_test_id = int(test_id)
                results = Result.objects.filter(test_id=selected_test_id, test__in=tests_qs)

            results = results.select_related("user", "test").order_by("-date_taken")

            # --- Агрегаты ---
            summary = None
            if results.exists():
                agg = results.aggregate(avg=Avg("score"), total=Count("id"))
                summary = {
                    "avg_score": round(agg["avg"] or 0, 2),
                    "attempts": agg["total"] or 0
                }

            context = {
                "mode": "teacher",
                "tests": tests_qs,
                "results": results,
                "summary": summary,
                "selected_test_id": selected_test_id,
            }
            return render(request, "tests/statistics.html", context)

        else:
            # --- Для студента ---
            results = Result.objects.filter(user=user).select_related("test").order_by("-date_taken")
            return render(request, "tests/statistics.html", {
                "mode": "student",
                "results": results
            })


class ExportStatisticsView(LoginRequiredMixin, TeacherRequiredMixin, View):
    """Выгрузка статистики в Excel или PDF, с учётом фильтра теста."""

    def get(self, request):
        format_type = request.GET.get("format", "excel")
        test_id = request.GET.get("test")

        # === Логика фильтрации ===
        if not test_id or test_id == "None":
            results = Result.objects.filter(test__author=request.user).select_related("test", "user")
        else:
            try:
                test = Test.objects.get(pk=int(test_id), author=request.user)
                results = Result.objects.filter(test=test).select_related("test", "user")
            except (ValueError, Test.DoesNotExist):
                return HttpResponse("Некорректный тест", status=400)

        # === EXCEL ===
        if format_type == "excel":
            wb = Workbook()
            ws = wb.active
            ws.title = "Статистика"

            headers = ["Дата", "Тест", "Пользователь", "Группа", "Попытка", "Баллы", "%", "Пройден"]
            ws.append(headers)

            for r in results:
                ws.append([
                    timezone.localtime(r.date_taken).strftime("%d.%m.%Y %H:%M"),
                    r.test.title,
                    r.user.username,
                    getattr(r, "group", "-") or "-",
                    r.attempt,
                    f"{r.score}/{r.total}",
                    f"{r.percentage}%",
                    "Да" if r.passed else "Нет"
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="statistics_test_{test_id or "all"}.xlsx"'
            )
            wb.save(response)
            return response

        # === PDF ===
        elif format_type == "pdf":
            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="statistics_test_{test_id or "all"}.pdf"'
            )

            # --- Шрифт DejaVuSans ---
            font_path = os.path.join(settings.BASE_DIR, "static", "fonts", "DejaVuSans", "DejaVuSans.ttf")
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
                font_name = "DejaVuSans"
            else:
                font_name = "Helvetica"

            doc = SimpleDocTemplate(
                response,
                pagesize=landscape(A4),
                rightMargin=1 * cm, leftMargin=1 * cm,
                topMargin=1 * cm, bottomMargin=1 * cm
            )

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name="TitleRu", parent=styles["Title"], fontName=font_name, fontSize=16, alignment=1))

            elements = [
                Paragraph("Статистика тестов", styles["TitleRu"]),
                Spacer(1, 12)
            ]

            data = [["Дата", "Тест", "Пользователь", "Группа", "Попытка", "Баллы", "%", "Пройден"]]
            for r in results:
                data.append([
                    timezone.localtime(r.date_taken).strftime("%d.%m.%Y %H:%M"),
                    r.test.title,
                    r.user.username,
                    getattr(r, "group", "-") or "-",
                    r.attempt,
                    f"{r.score}/{r.total}",
                    f"{r.percentage}%",
                    "Да" if r.passed else "Нет"
                ])

            table = Table(data, colWidths=[3 * cm, 5 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm])
            table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgreen),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
            ]))

            elements.append(table)
            doc.build(elements)
            return response

        return HttpResponse("Unsupported format", status=400)
