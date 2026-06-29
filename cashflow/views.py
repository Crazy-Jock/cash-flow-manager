from django.shortcuts import render
from django.http import JsonResponse

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