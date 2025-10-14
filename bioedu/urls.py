from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# DRF JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # Переключатель языка

    # JWT endpoints (вне i18n)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Основные URL
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('users/', include('users.urls')),
    path('tests/', include('tests.urls')),
    path('theory/', include('theory.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),

    # DRF endpoints
    path("api/tests/", include("tests.api.urls")), # tests API
    path("api/theory/", include("theory.api.urls")), # theory API
    path("api/users/", include("users.api.urls")), # users API
)

# Для статики и медиа
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
