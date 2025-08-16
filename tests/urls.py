from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('create/', views.create_test, name='create_test'),
    path('manage/', views.manage_tests, name='manage_tests'),
    path('<int:test_id>/take/', views.take_test, name='take_test'),
    path('<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path("statistics/", views.statistics, name="statistics"),
]
