from django.shortcuts import render, redirect
from theory.models import Section  # импортируем модели теории

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")  # если не авторизован — на логин
    sections = Section.objects.all()
    return render(request, "index.html", {"sections": sections})

def section_list(request):
    sections = Section.objects.all()
    return render(request, "section_list.html", {"sections": sections})
