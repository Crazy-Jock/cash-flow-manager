from django.urls import path

from cashflow import views


urlpatterns = [
    path("", views.cashflow_list, name="list"), # главная страница с таблицей записей ДДС
]