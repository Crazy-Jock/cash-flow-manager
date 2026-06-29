from django import forms
from cashflow.models import CashFlow, Category, SubCategory


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = "__all__"
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

        self.fields["category"].queryset = Category.objects.none()
        self.fields["subcategory"].queryset = SubCategory.objects.none()