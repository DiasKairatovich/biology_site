from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Переключатель языка
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')), # Главная страница и прочее
    path('users/', include('users.urls')), # Пользователи
    path('tests/', include('tests.urls')), # Тесты
    path('theory/', include('theory.urls')),
)

# Для статики
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
