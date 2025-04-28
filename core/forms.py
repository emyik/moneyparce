# core/forms.py
from django import forms
from .models import Transaction
from .models import Budget
from .models import Category

class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class BudgetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BudgetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Budget
        fields = ['category', 'amount']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']