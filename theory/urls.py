from django.urls import path
from . import views

urlpatterns = [
    path("<int:section_id>/", views.section_detail, name="section_detail"),  # конкретный раздел
    path("topic/<int:topic_id>/", views.topic_detail, name="topic"),         # конкретная тема
]
