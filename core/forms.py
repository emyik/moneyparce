# core/forms.py
from django import forms
from .models import Transaction
from .models import Budget
from .models import Category

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']