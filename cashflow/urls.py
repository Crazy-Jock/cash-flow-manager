from django.urls import path

from cashflow import views


urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"), # главная страница с таблицей записей ДДС
    path("ajax/categories/", views.get_categories), # для получения JsonResponse вида категорий, после выбора "Тип" в фильтре
    path("ajax/subcategories/", views.get_subcategories), # для получения JsonResponse вида подкатегорий, после выбора категории в фильтре

    path("create/", views.cashflow_create, name="cashflow_create"), # страница с формой для создания новой записи
    path("edit/<int:id>/", views.cashflow_edit, name="cashflow_edit"), # страница с формой для редактирования текущей записи
    path("delete/<int:id>/", views.cashflow_delete, name="cashflow_delete"), # для удаления записи ДДС из БД
]