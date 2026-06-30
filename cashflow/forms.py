from django import forms
from cashflow.models import CashFlow, Category, Status, SubCategory, Type


# форма для создания/редактирования записи ДДС
class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = "__all__"
        
        widgets = {
            "type": forms.Select(attrs={"id": "type-select"}),
            "category": forms.Select(attrs={"id": "category-select"}),
            "subcategory": forms.Select(attrs={"id": "subcategory-select"}),
        }
        
        # для лучшего понимания понятные таблички
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


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = "__all__"

        # для лучшего понимания понятная табличка
        label = {"name": "Статус"}

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = "__all__"

        # для лучшего понимания понятная табличка
        label = {"name": "Тип"}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

        # для лучшего понимания понятные таблички
        labels = {
            "type": "Тип",
            "name": "Категория",
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = "__all__"

        # для лучшего понимания понятные таблички
        labels = {
            "category": "Категория",
            "name": "Подкатегория",
        }