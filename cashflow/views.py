from django import forms
from django.db import models
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib import messages as django_messages

from cashflow.forms import CashFlowForm, CategoryForm, StatusForm, SubCategoryForm, TypeForm
from cashflow.models import Type, Status, Category, SubCategory, CashFlow


# создание таблицы для отображения записей ДДС
def cashflow_list(request: HttpRequest) -> HttpResponse:
    # получение всех записей ДДС из БД
    items = CashFlow.objects.all().select_related(
        "status", "type", "category", "subcategory"
    )

    # создание параметров get для фильтрации таблицы
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    status = request.GET.get("status")
    selected_type = request.GET.get("type")
    selected_category = request.GET.get("category")
    selected_subcategory = request.GET.get("subcategory")

    # фильтрация записей в таблице
    if date_from:
        items = items.filter(created_at__gte=date_from)
    if date_to:
        items = items.filter(created_at__lte=date_to)
    if status:
        items = items.filter(status_id=status)
    if selected_type:
        items = items.filter(type_id=selected_type)
    if selected_type and selected_category:
        items = items.filter(category_id=selected_category)
    if selected_type and selected_category and selected_subcategory:
        items = items.filter(subcategory_id=selected_subcategory)

    categories_for_select = (
        Category.objects.filter(type_id=selected_type)
        if selected_type
        else Category.objects.none()
    )

    subcategories_for_select = (
        SubCategory.objects.filter(category_id=selected_category)
        if selected_category
        else SubCategory.objects.none()
    )

    # рендер главной страницы без/с фильтрами
    return render(request, "cashflow/list.html", {"items": items.order_by("created_at"),
                                                  "status": Status.objects.all(),
                                                  "type": Type.objects.all(),
                                                  "categories_for_select": categories_for_select,
                                                  "subcategories_for_select": subcategories_for_select,
                                                  "filters": request.GET,}) # чтобы сохранять выбранные фильтры

# получение словаря категорий, после выбора "Тип" в фильтре
def get_categories(request: HttpRequest) -> JsonResponse:
    # получение типа из запроса
    selected_type = request.GET.get("type")
    # если "Тип" в фильтре станет снова пустым
    if not selected_type:
        return JsonResponse([], safe=False)

    # получение всех категорий из БД, которые относятся к выбранному типу
    categories = Category.objects.filter(type_id=selected_type).values("id", "name")

    return JsonResponse(list(categories), safe=False)

# получение словаря подкатегорий, после выбора категории в фильтре
def get_subcategories(request: HttpRequest) -> JsonResponse:
    # получение категории из запроса
    selected_category = request.GET.get("category")
    # если категория в фильтре снова станет пустой
    if not selected_category:
        return JsonResponse([], safe=False)
    # получение всех подкатегорий из БД, которые относятся к выбранной категории
    subcategories = SubCategory.objects.filter(category_id=selected_category).values("id", "name")
    
    return JsonResponse(list(subcategories), safe=False)


# создание новой записи ДДС в БД
def cashflow_create(request: HttpRequest) -> HttpResponse:
    form = CashFlowForm(request.POST or None)

    # если введенные данные валидные, то сохранить новую запись ДДС в БД и вернуть пользователя на главную страницу
    if form.is_valid():
        form.save()
        return redirect("cashflow_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})

# редактирование записи ДДС в БД
def cashflow_edit(request: HttpRequest, id: int) -> HttpResponse:
    # получаем запись ДДС из БД
    item = CashFlow.objects.get(id=id)
    form = CashFlowForm(request.POST or None, instance=item)

    # если введенные данные валидные, то обновить существующую запись ДДС в БД
    if form.is_valid():
        form.save()
        return redirect("cashflow_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})

# удаление записи ДДС из БД
def cashflow_delete(request: HttpRequest, id: int) -> HttpResponse:
    CashFlow.objects.filter(id=id).delete()

    return redirect("cashflow_list")


# создание таблицы-справочника со статусами, типами, категориями и подкатегориями
def directory_list(request) -> HttpResponse:
    # рендер справочника со всеми статусами, типами, категориями и подкатегориями
    return render(request, "cashflow/directory.html", {"status": Status.objects.all().order_by("name"),
                                                       "type": Type.objects.all().order_by("name"),
                                                       "category": Category.objects.all().order_by("name"),
                                                       "subcategory": SubCategory.objects.all().order_by("name")})

# универсальная функция для создания статуса/типа/категории/подкатегории в БД
def directory_create_object(request: HttpRequest, form_object) -> HttpResponse:
    # получаем какую-либо форму
    form = form_object(request.POST or None)

    # если введенные данные валидные, то сохранить новый статус/тип/категорию/подкатегорию и вернуть пользователя в справочник
    if form.is_valid():
        form.save()
        return redirect("directory_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})

# универсальная функция для редактирования статуса/типа/категории/подкатегории из БД
def directory_edit_object(request: HttpRequest, 
                          form_object: forms.ModelForm, 
                          model_object: models.Model, 
                          id: int) -> HttpResponse:
    # получаем какую-либо заполненную форму
    item = get_object_or_404(model_object, id=id) # вернуть 404 страницу, если объект не найден
    form = form_object(request.POST or None, instance=item)

    # если введенные данные валидные, то отредактировать статус/тип/категорию/подкатегорию и вернуть пользователя в справочник
    if form.is_valid():
        form.save()
        return redirect("directory_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})

# универсальная функция для удаления статуса/типа/категории/подкатегории из БД
def directory_delete_object(request: HttpRequest, 
                            model_object: models.Model, 
                            id: int) -> HttpResponse:
    item = get_object_or_404(model_object, id=id) # вернуть 404 страницу, если объект не найден

    try:
        item.delete()
    except ProtectedError:
        django_messages.error(request, f"Нельзя удалить {item.name}. Есть связанные записи")

    return redirect("directory_list")

# создание нового статуса в БД
def create_status(request: HttpRequest) -> HttpResponse:
    return directory_create_object(request, StatusForm)

# создание нового типа в БД
def create_type(request: HttpRequest) -> HttpResponse:
    return directory_create_object(request, TypeForm)

# создание новой категории
def create_category(request: HttpRequest) -> HttpResponse:
    return directory_create_object(request, CategoryForm)

# создание новой подкатегории
def create_subcategory(request: HttpRequest) -> HttpResponse:
    return directory_create_object(request, SubCategoryForm)

# редактирование статуса из БД
def edit_status(request: HttpRequest, id: int) -> HttpResponse:
    return directory_edit_object(request, StatusForm, Status, id)

# редактирование типа из БД
def edit_type(request: HttpRequest, id: int) -> HttpResponse:
    return directory_edit_object(request, TypeForm, Type, id)

# редактирование категории из БД
def edit_category(request: HttpRequest, id: int) -> HttpResponse:
    return directory_edit_object(request, CategoryForm, Category, id)

# редактирование подкатегории из БД
def edit_subcategory(request: HttpRequest, id: int) -> HttpResponse:
    return directory_edit_object(request, SubCategoryForm, SubCategory, id)

# удаление статуса из БД
def delete_status(request: HttpRequest, id) -> HttpResponse:
    return directory_delete_object(request, Status, id)

# удаление типа из БД
def delete_type(request: HttpRequest, id) -> HttpResponse:
    return directory_delete_object(request, Type, id)

# удаление категории из БД
def delete_category(request: HttpRequest, id) -> HttpResponse:
    return directory_delete_object(request, Category, id)

# удаление подкатегории из БД
def delete_subcategory(request: HttpRequest, id) -> HttpResponse:
    return directory_delete_object(request, SubCategory, id)