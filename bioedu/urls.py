from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница и прочее
    path('', include('main.urls')),

    # Пользователи
    path('users/', include('users.urls')),

    # Тесты
    path('tests/', include('tests.urls')),
]

# Для статики
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
