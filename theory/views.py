from django.shortcuts import render, get_object_or_404
from .models import Section, Topic

def section_detail(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    topics = section.topics.all()  # уже отсортированы по Meta.ordering
    current_topic = topics.first()  # открываем первую тему по умолчанию

    return render(request, "section.html", {
        "section": section,
        "topics": topics,
        "current_topic": current_topic,
    })


def topic_detail(request, topic_id):
    current_topic = get_object_or_404(Topic, id=topic_id)
    section = current_topic.section
    topics = section.topics.all()  # чтобы боковое меню показывало все темы раздела

    return render(request, "section.html", {
        "section": section,
        "topics": topics,
        "current_topic": current_topic,
    })
