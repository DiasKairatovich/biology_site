from django.urls import path
from . import views

urlpatterns = [
    # --- Разделы ---
    path("sections/", views.section_list, name="section_list"),              # список всех разделов (видят все)
    path("sections/manage/", views.manage_sections, name="manage_sections"),  # управление разделами (только учителя)
    path("sections/create/", views.create_section, name="create_section"),   # создать раздел
    path("sections/<int:section_id>/edit/", views.edit_section, name="edit_section"),  # редактировать раздел
    path("sections/<int:section_id>/delete/", views.delete_section, name="delete_section"),  # удаление раздела

    # --- Темы ---
    path("section/<int:section_id>/", views.section_detail, name="section_detail"),  # конкретный раздел
    path("section/<int:section_id>/add-topic/", views.create_topic, name="create_topic"),   # создать тему
    path("topic/<int:topic_id>/edit/", views.edit_topic, name="edit_topic"),   # редактировать тему
    path("topic/<int:topic_id>/", views.topic_detail, name="topic"),   # конкретная тема
]
