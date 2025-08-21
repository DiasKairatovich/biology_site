from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sections/", views.section_list, name="section_list"),  # список всех разделов
]
