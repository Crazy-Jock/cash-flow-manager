from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls), # страница админки
    path("", include("cashflow.urls")), # главная страница с таблицей записей ДДС
]
