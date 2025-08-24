from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, Topic
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import TopicForm, SectionForm
from django.contrib import messages

@login_required
def section_list(request):
    sections = Section.objects.all()
    is_teacher = request.user.groups.filter(name="Учителя").exists()
    return render(
        request,
        "theory/section_list.html",
        {"sections": sections, "is_teacher": is_teacher},
    )

@login_required
def manage_sections(request):
    if not request.user.groups.filter(name="Учителя").exists():
        messages.error(request, "Только учителя могут управлять разделами.")
        return redirect("section_list")

    sections = Section.objects.all()
    return render(request, "theory/manage_sections.html", {"sections": sections})

@login_required
def create_section(request):
    if not request.user.groups.filter(name="Учителя").exists():
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
    if not request.user.groups.filter(name="Учителя").exists():
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
def delete_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if not request.user.groups.filter(name="Учителя").exists():
        return redirect("section_list")

    if request.method == "POST":
        section.delete()
        messages.success(request, "Раздел удалён!")
        return redirect("manage_sections")

    return render(request, "theory/confirm_delete_section.html", {"section": section})

@login_required
def create_topic(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.section = section
            topic.save()
            return redirect("section_detail", section_id=section.id)
    else:
        form = TopicForm()
    return render(request, "theory/topic_form.html", {"form": form, "section": section})


@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == "POST":
        form = TopicForm(request.POST, request.FILES, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("topic", topic_id=topic.id)
    else:
        form = TopicForm(instance=topic)
    return render(request, "theory/topic_form.html", {"form": form, "section": topic.section})

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