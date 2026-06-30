from django.urls import path

from cashflow import views


urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"), # главная страница с таблицей записей ДДС
    path("ajax/categories/", views.get_categories), # для получения JsonResponse вида категорий, после выбора "Тип" в фильтре
    path("ajax/subcategories/", views.get_subcategories), # для получения JsonResponse вида подкатегорий, после выбора категории в фильтре

    path("create/", views.cashflow_create, name="cashflow_create"), # страница с формой для создания новой записи
    path("edit/<int:id>/", views.cashflow_edit, name="cashflow_edit"), # страница с формой для редактирования текущей записи
    path("delete/<int:id>/", views.cashflow_delete, name="cashflow_delete"), # для удаления записи ДДС из БД

    path("directories/", views.directory_list, name="directory_list"), # страница-справочник для создания/редактирования/удаления типов/категорий/подкатегорий

    path("directories/status/create/", views.create_status, name="create_status"), # страница с формой для создания нового статуса
    path("directories/type/create/", views.create_type, name="create_type"), # страница с формой для создания нового типа
    path("directories/category/create/", views.create_category, name="create_category"), # страница с формой для создания новой категории
    path("directories/subcategory/create/", views.create_subcategory, name="create_subcategory"), # страница с формой для создания новой подкатегории

    path("directories/status/edit/<int:id>", views.edit_status, name="edit_status"), # страница с формой для редактирования статуса
    path("directories/type/edit/<int:id>", views.edit_type, name="edit_type"), # страница с формой для редактирования типа
    path("directories/category/edit/<int:id>", views.edit_category, name="edit_category"), # страница с формой для редактирования категории
    path("directories/subcategory/edit/<int:id>", views.edit_subcategory, name="edit_subcategory"), # страница с формой для редактирования подкатегории
    
    path("directories/status/delete/<int:id>", views.delete_status, name="delete_status"), # для удаления статуса
    path("directories/type/delete/<int:id>", views.delete_type, name="delete_type"), # для удаления типа
    path("directories/category/delete/<int:id>", views.delete_category, name="delete_category"), # для удаления категории
    path("directories/subcategory/delete/<int:id>", views.delete_subcategory, name="delete_subcategory"), # для удаления подкатегории
]