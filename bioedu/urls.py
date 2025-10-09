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
    path('', include('main.urls')), # главная страница и прочее
    path('users/', include('users.urls')), # пользователи
    path('tests/', include('tests.urls')), # тесты
    path('theory/', include('theory.urls')), # теория
    path("ckeditor/", include("ckeditor_uploader.urls")), # окно редактора

    # Новый API
    path('api/', include('tests.api.urls')),
)

# Для статики
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
