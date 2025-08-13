from django.shortcuts import render, redirect

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')  # если не авторизован — на логин
    sections = [
        "Раздел 1: Клетка",
        "Раздел 2: Генетика",
        "Раздел 3: Экология",
        "Раздел 4: Анатомия"
    ]
    return render(request, 'index.html', {'sections': sections})
def section(request):
    return render(request, 'section.html')
