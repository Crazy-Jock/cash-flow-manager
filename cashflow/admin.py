from django.contrib import admin

from cashflow.models import Type, Status, Category, SubCategory, CashFlow


admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(CashFlow)