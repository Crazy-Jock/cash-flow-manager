from django import forms
from cashflow.models import CashFlow, Category, SubCategory


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = "__all__"
        
        widgets = {
            "type": forms.Select(attrs={"id": "type-select"}),
            "category": forms.Select(attrs={"id": "category-select"}),
            "subcategory": forms.Select(attrs={"id": "subcategory-select"}),
        }
        
        # для лучшего понимания
        labels = {
            "created_at": "Дата",
            "status": "Статус",
            "type": "Тип",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "amount": "Кээш",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.all()
        self.fields["subcategory"].queryset = SubCategory.objects.all()