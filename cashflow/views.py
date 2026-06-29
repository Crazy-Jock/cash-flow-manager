from django.shortcuts import render, redirect
from django.http import JsonResponse

from cashflow.forms import CashFlowForm
from cashflow.models import Type, Status, Category, SubCategory, CashFlow


# создание таблицы для отображения записей ДДС
def cashflow_list(request):
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
    return render(request, "cashflow/list.html", {"items": items,
                                                  "status": Status.objects.all(),
                                                  "type": Type.objects.all(),
                                                  "categories_for_select": categories_for_select,
                                                  "subcategories_for_select": subcategories_for_select,
                                                  "filters": request.GET,}) # чтобы сохранять выбранные фильтры

# получение словаря категорий, после выбора "Тип" в фильтре
def get_categories(request) -> JsonResponse:
    # получение типа из запроса
    selected_type = request.GET.get("type")
    # если "Тип" в фильтре станет снова пустым
    if not selected_type:
        return JsonResponse([], safe=False)

    # получение всех категорий из БД, которые относятся к выбранному типу
    categories = Category.objects.filter(type_id=selected_type).values("id", "name")

    return JsonResponse(list(categories), safe=False)

# получение словаря подкатегорий, после выбора категории в фильтре
def get_subcategories(request) -> JsonResponse:
    # получение категории из запроса
    selected_category = request.GET.get("category")
    # если категория в фильтре снова станет пустой
    if not selected_category:
        return JsonResponse([], safe=False)
    # получение всех подкатегорий из БД, которые относятся к выбранной категории
    subcategories = SubCategory.objects.filter(category_id=selected_category).values("id", "name")
    
    return JsonResponse(list(subcategories), safe=False)

# создание новой записи ДДС в БД
def cashflow_create(request):
    form = CashFlowForm(request.POST or None)

    # если введенные данные валидные, то сохранить новую запись ДДС в БД и вернуть пользователя на главную страницу
    if form.is_valid():
        form.save()
        return redirect("cashflow_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})


# редактирование записи ДДС в БД
def cashflow_edit(request, id):
    # получаем запись ДДС из БД
    item = CashFlow.objects.get(id=id)
    form = CashFlowForm(request.POST or None, instance=item)

    # если введенные данные валидные, то обновить существующую запись ДДС в БД
    if form.is_valid():
        form.save()
        return redirect("cashflow_list")
    
    # если введенные данные не валидные, то вернуть пользователя снова к заполнению формы
    return render(request, "cashflow/form.html", {"form": form})