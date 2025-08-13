from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')), # Главная страница и прочее
    path('users/', include('users.urls')), # Пользователи
    path('tests/', include('tests.urls')), # Тесты
]

# Для статики
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
