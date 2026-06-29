from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=127)

    # для удобного отображения в админке
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=127)

    # для удобного отображения в админке
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=127)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    # для удобного отображения в админке
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=127)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # для удобного отображения в админке
    def __str__(self):
        return self.name

class CashFlow(models.Model):
    created_at = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    # для удобного отображения в админке
    def __str__(self):
        return f"{self.status} | {self.type}/{self.category}/{self.subcategory}"