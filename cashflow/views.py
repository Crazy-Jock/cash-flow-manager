from django.shortcuts import render

from cashflow.models import Type, Status, Category, SubCategory, CashFlow


# создание таблицы для отображения записей ДДС
def cashflow_list(request):
    # получение всех записей ДДС из БД
    items = CashFlow.objects.all().select_related("status", "type", 
                                                  "category", "subcategory")
    
    # рендер шаблона с передачей в него записей ДДС
    return render(request, "cashflow/list.html", {"items": items})
