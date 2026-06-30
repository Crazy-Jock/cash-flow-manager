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
            "amount": forms.NumberInput(attrs={"min": "0"}) # чтобы пользователю нельзя было прописать сумму меньше 0
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

    # функция для валидации данных, чтобы проверить связи тип<-категория и категория<-подкатегория
    def clean(self):
        cleaned_data = super().clean()

        # получаем данные после встроенной валидации django
        type_ = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")
        amount = cleaned_data.get("amount")
        
        # проверка принадлежности выбранной категории к выбранному типу
        if type_ and category:
            if category.type != type_:
                self.add_error("category", "Выбранная категория не принадлежить выбранному типу")
        # проверка принадлежности выбранной пожкатегории к выбранной категории
        if category and subcategory:
            if subcategory.category != category:
                self.add_error("subcategory", "Выбранная подкатегория не принадлежит выбранной категории")
        # проверка на положительную сумму
        if (amount is not None) and (amount < 0):
            self.add_error("amount", "Кэш не может быть отрицательным")
        
        # возвращаем валидированные данные, после собственной проверки
        return cleaned_data


# форма для создания/редактирования статуса
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = "__all__"

        # для лучшего понимания понятная табличка
        label = {"name": "Статус"}

# форма для создания/редактирования типа
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = "__all__"

        # для лучшего понимания понятная табличка
        label = {"name": "Тип"}

# форма для создания/редактирования категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

        # для лучшего понимания понятные таблички
        labels = {
            "type": "Тип",
            "name": "Категория",
        }

# форма для создания/редактирования подкатегории
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = "__all__"

        # для лучшего понимания понятные таблички
        labels = {
            "category": "Категория",
            "name": "Подкатегория",
        }