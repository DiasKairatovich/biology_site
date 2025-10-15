from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, Topic
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TopicForm, SectionForm
from django.contrib import messages

def is_teacher(user):
    return user.is_authenticated and user.role == "teacher"

@login_required
def section_list(request):
    sections = Section.objects.all()
    is_teacher = request.user.role == "teacher"
    return render(
        request,
        "theory/section_list.html",
        {"sections": sections, "is_teacher": is_teacher},
    )

@login_required
def manage_sections(request):
    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут управлять разделами.")
        return redirect("section_list")

    sections = Section.objects.all()
    return render(request, "theory/manage_sections.html", {"sections": sections})

@login_required
def create_section(request):
    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут создавать разделы.")
        return redirect("section_list")

    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Раздел создан!")
            return redirect("manage_sections")
    else:
        form = SectionForm()

    return render(request, "theory/section_form.html", {"form": form})

@login_required
def edit_section(request, section_id):
    section = get_object_or_404(Section, pk=section_id)
    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут редактировать разделы.")
        return redirect("section_list")

    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Раздел обновлён!")
            return redirect("manage_sections")
    else:
        form = SectionForm(instance=section)

    return render(request, "theory/section_form.html", {"form": form})

@login_required
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут удалять разделы.")
        return redirect("section_list")

    if request.method == "POST":
        section.delete()
        messages.success(request, "Раздел удалён!")
        return redirect("manage_sections")

    return render(request, "theory/confirm_delete_section.html", {"section": section})

@login_required
def section_detail(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    topics = section.topics.all()  # уже отсортированы по Meta.ordering
    current_topic = topics.first() if topics.exists() else None # открываем первую тему по умолчанию

    return render(request, "theory/section.html", {
        "section": section,
        "topics": topics,
        "current_topic": current_topic,
    })

@login_required
def create_topic(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут создавать темы.")
        return redirect("section_detail", section_id=section.id)

    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.section = section
            topic.save()
            messages.success(request, "Тема создана!")
            return redirect("section_detail", section_id=section.id)
    else:
        form = TopicForm()

    return render(request, "theory/topic_form.html", {"form": form, "section": section})


@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут редактировать темы.")
        return redirect("topic_detail", topic_id=topic.id)

    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, "Тема обновлена!")
            return redirect("topic", topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)

    return render(request, "theory/topic_form.html", {"form": form, "section": topic.section})

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if not is_teacher(request.user):
        messages.error(request, "Только учителя могут удалять темы.")
        return redirect("topic", topic_id=topic.id)

    if request.method == "POST":
        section_id = topic.section.id
        topic.delete()
        messages.success(request, "Тема удалена!")
        return redirect("section_detail", section_id=section_id)

    return render(request, "theory/confirm_delete_topic.html", {"topic": topic})

@login_required
def topic_detail(request, topic_id):
    current_topic = get_object_or_404(Topic, id=topic_id)
    section = current_topic.section
    topics = section.topics.all()  # чтобы боковое меню показывало все темы раздела

    return render(request, "theory/section.html", {
        "section": section,
        "topics": topics,
        "current_topic": current_topic,
    })

@login_required
def topic_detail_slug(request, slug):
    current_topic = get_object_or_404(Topic, slug=slug)
    section = current_topic.section
    topics = section.topics.all()

    return render(request, "theory/section.html", {
        "section": section,
        "topics": topics,
        "current_topic": current_topic,
    })
