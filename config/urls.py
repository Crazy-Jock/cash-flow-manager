from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls), # страница админки
    path("", include("cashflow.urls")), # эндпоинты для cashflow (главная страница, справочник, формы и т.д.)
]
