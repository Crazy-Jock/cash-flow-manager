from django.shortcuts import render

from cashflow.models import Type, Status, Category, SubCategory, CashFlow


def cashflow_list(request):
    items = CashFlow.objects.all().select_related("status", "type", 
                                                  "category", "subcategory")
    
    return render(request, "cashflow/list.html", {"items": items})
