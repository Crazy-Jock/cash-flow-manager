from django.urls import path

from cashflow import views


urlpatterns = [
    path("", views.cashflow_list, name="list"), # главная страница с таблицей записей ДДС
    path("ajax/categories/", views.get_categories), # для получения JsonResponse вида категорий, после выбора "Тип" в фильтре
    path("ajax/subcategories/", views.get_subcategories), # для получения JsonResponse вида подкатегорий, после выбора категории в фильтре
]